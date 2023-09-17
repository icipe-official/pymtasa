import os

import csv
import numpy as np


class Utils:
    @staticmethod
    def remove_duplicates(lst: list) -> list:
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]

    @staticmethod
    def compute_rotation_coefficient(rotation_mode: bool, analysis_period: list[int], reference_vector: np.ndarray,
                                     target_env_data_row: np.ndarray) -> float:
        if len(target_env_data_row) == 1:
            return 0

        n = reference_vector.shape[1] if reference_vector.ndim != 1 else len(reference_vector)

        if rotation_mode:
            indices = np.array(analysis_period) - 1
            if reference_vector.ndim == 1:
                analysis_reference_vector = np.zeros(n)
                analysis_reference_vector[range(len(indices))] = reference_vector[indices]
                fourier1 = np.fft.fft(analysis_reference_vector)
                fourier2 = np.fft.fft(target_env_data_row)
            else:
                analysis_reference_matrix = np.zeros((2, n))
                analysis_reference_matrix[0, range(len(indices))] = reference_vector[0, :][indices]
                analysis_reference_matrix[1, range(len(indices))] = reference_vector[1, :][indices]
                fourier1 = np.sum(np.fft.fft(analysis_reference_matrix), axis=0)
                fourier2 = np.sum(np.fft.fft(target_env_data_row), axis=0)
            return (n - np.real(np.fft.ifft(np.conjugate(fourier2) * fourier1)).argmax()) % n
        else:
            if reference_vector.ndim == 1:
                fourier1 = np.fft.fft(reference_vector)
                fourier2 = np.fft.fft(target_env_data_row)
            else:
                fourier1 = np.sum(np.fft.fft(reference_vector), axis=0)
                fourier2 = np.sum(np.fft.fft(target_env_data_row), axis=0)

            highest_frequency_component_pos_fourier1 = np.argmax(np.abs(fourier1[1:]))

            if highest_frequency_component_pos_fourier1 == np.argmax(np.abs(fourier2[1:])):
                phase1 = np.angle(fourier1)
                phase2 = np.angle(fourier2)
                return round(((phase1[highest_frequency_component_pos_fourier1 + 1] - phase2[
                    highest_frequency_component_pos_fourier1 + 1]) * (n / 2)) / np.pi, 0) % n
            else:
                return (n - np.real(np.fft.ifft(np.multiply(fourier1, np.conjugate(fourier2)))).argmax()) % n

    @staticmethod
    def perform_distance_normalization(distances: np.ndarray, normalization_coefficient: int) -> np.array:
        return normalization_coefficient / (normalization_coefficient + distances)

    @staticmethod
    def convert_time_series_dataset_into_matrix_list(target_data: list[str],
                                                     headers_indices: list[list[int]]) -> list[np.ndarray]:
        matrix_list = [Utils.csv_into_matrix(file_path, headers_indices[i]) for i, file_path in enumerate(target_data)]
        return matrix_list

    @staticmethod
    def csv_into_matrix(file_path: str, headers_indices: list[int]) -> np.ndarray:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            matrix = [[row[i] for i in headers_indices] for row in reader]
        return np.array(matrix, dtype=np.float64)

    @staticmethod
    def convert_time_series_dataset_into_matrix(target_data: list[str], headers_indices: list[list[int]]) -> np.ndarray:
        matrix = None
        for i, csv_file in enumerate(target_data):
            values = Utils.csv_into_matrix(csv_file, headers_indices[i])
            if matrix is None:
                matrix = values
            else:
                matrix = np.column_stack((matrix, values))
        return matrix

    @staticmethod
    def create_csv_file_from_matrix(matrix: np.ndarray, directory: str, csv_name: str, headers: list[str]) -> str:
        file_path = os.path.join(directory, csv_name)
        with open(file_path, 'w', newline='') as csvfile:
            csvfile.write(','.join(headers) + '\n')
            np.savetxt(csvfile, matrix, delimiter=',', fmt='%.2f')
        return file_path

