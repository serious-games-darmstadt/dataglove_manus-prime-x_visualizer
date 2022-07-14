import subprocess
import shutil
import fileinput
import os
import json
from pathlib import Path


PARENT_DIR = Path(__file__).parent.resolve()


class DynamicDataVisualizer:
    SUPPORTED_OUT_FILE_TYPES = ['blend']

    def __init__(self, output_dir: str = os.path.join(PARENT_DIR, R"../dynamic")) -> None:
        self.label = ""
        self.hand = ""
        self.gesture_data = {}  # json data of interval for dynamic gesture
        self.blender_path = R"/Applications/Blender.app/Contents/MacOS/Blender"  # shutil.which('blender')
        self.blender_script_path = os.path.join(PARENT_DIR, R"./blender_script_dynamic.py")
        self.output_dir = os.path.abspath(output_dir)

        Path(output_dir).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def __check_input_file_type(json_path: str) -> bool:
        return True if json_path.endswith('.json') else False

    def generate_dynamic_gesture(self, json_path: str, export: bool) -> None:
        """
        Generates the dynamic gesture from the json data and the given label. Either save the result
        as file or open it directly in blender.
        :param json_path:
        :param export:
        :return:
        """
        print("Generating dynamic gesture ...")

        # Assert input
        if self.blender_path is None:
            print("Blender must be installed and in path!")
            return

        if not self.__check_input_file_type(json_path):
            print("Json file needed as input!")
            return

        with open(json_path, 'r') as f:
            gesture_data = json.load(f)
        if not gesture_data:
            print("This label is not present in the json data!")
            return

        # Set attributes
        self.__reset()
        self.gesture_data = gesture_data
        self.label = gesture_data[0]["letter"]
        self.hand = gesture_data[0]["hand"]

        # Build and run dynamic blender script for each gesture
        for i, d in enumerate(self.gesture_data):
            print('hey', i)
            self.iteration = i
            self.__create_dynamic_blender_script(d, export)
            self.__run_dynamic_blender_script(export)
            self.__reset_dynamic_blender_script(d, export)

        print("Finished generating dynamic gesture(s)!")

    def __create_dynamic_blender_script(self, gesture_data: dict, export: bool) -> None:
        # Replace export variable in blender_script_dynamic.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace("EXPORT = None", f"EXPORT = '{str(export)}'").rstrip())

        # Replace label variable in blender_script_dynamic.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace("LABEL = ''", f"LABEL = '{self.label}'").rstrip())

        # Replace hand variable in blender_script_dynamic.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace("HAND = ''", f"HAND = '{self.hand}'").rstrip())

        # Replace gesture_data variable in blender_script_dynamic.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace("gesture_data = {}", f"gesture_data = {str(gesture_data)}").rstrip())

        # Replace export_file_type variable in blender_script_dynamic.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(
                "EXPORT_FILE_TYPE = ''", f"EXPORT_FILE_TYPE = 'blend'").rstrip())

        # Replace output path
        for output_file_type in self.SUPPORTED_OUT_FILE_TYPES:
            out_str = f"{output_file_type.upper()}_PATH_STR"
            old_output_path = f"{out_str} = ''"
            new_value = os.path.join(self.output_dir, f"dynamic_{self.label}_{self.hand}_{self.iteration}.{output_file_type}")
            new_output_path = f"{out_str} = R'{new_value}'"
            for line in fileinput.input(self.blender_script_path, inplace=True):
                print(line.replace(old_output_path, new_output_path).rstrip())

    def __reset_dynamic_blender_script(self, gesture_data: dict, export: bool) -> None:
        # Reset each change done in __create_dynamic_blender_script()
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(f"EXPORT = '{str(export)}'", "EXPORT = None").rstrip())
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(f"LABEL = '{self.label}'", "LABEL = ''").rstrip())
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(f"HAND = '{self.hand}'", "HAND = ''").rstrip())
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(f"gesture_data = {str(gesture_data)}", "gesture_data = {}").rstrip())
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(
                f"EXPORT_FILE_TYPE = 'blend'", "EXPORT_FILE_TYPE = ''").rstrip())

        for output_file_type in self.SUPPORTED_OUT_FILE_TYPES:
            out_str = f"{output_file_type.upper()}_PATH_STR"
            old_output_path = f"{out_str} = ''"
            new_value = os.path.join(self.output_dir, f"dynamic_{self.label}_{self.hand}_{self.iteration}.{output_file_type}")
            new_output_path = f"{out_str} = R'{new_value}'"
            for line in fileinput.input(self.blender_script_path, inplace=True):
                print(line.replace(new_output_path, old_output_path).rstrip())

    def __reset(self) -> None:
        self.label = ""
        self.hand = ""
        self.gesture_data = {}

    def __run_dynamic_blender_script(self, export: bool):
        args = [self.blender_path, "--background", "--python", self.blender_script_path]  # Build cmd line arguments
        if not export:
            args.remove("--background")
        subprocess.run(args)  # Run blender process with script


class StaticDataVisualizer:
    SUPPORTED_IN_FILE_TYPES = ['txt']
    SUPPORTED_OUT_FILE_TYPES = ['stl', 'blend', 'obj']

    def __init__(self,
                 blender_script_path: str = os.path.join(PARENT_DIR, R"./blender_script_static.py"),
                 output_dir: str = os.path.join(PARENT_DIR, R"../static")) -> None:
        self.label = ""
        self.hand = ""
        self.data_samples = []  # List of lists (multiple samples)
        self.input_file_name = R""
        self.blender_path =  R"/Applications/Blender.app/Contents/MacOS/Blender"  # shutil.which('blender')
        self.blender_script_path = blender_script_path
        self.output_dir = output_dir

        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def generate_static_gesture_from_file(self, file_path: str, file_type: str) -> None:
        """
        Generates three static gestures from the file with data in WACH format. The files must contain
        data for three gestures.
        :param file_path:
        :param file_type:
        :return:
        """
        print("Generating static gesture ...")

        # Assert arguments
        if self.blender_path is None:
            print("Blender must be installed and in path!")
            return

        if file_type not in self.SUPPORTED_OUT_FILE_TYPES:
            print("File type for export not supported!")

        self.__read_from_file(file_path)
        self.__export_as(file_type)

        print("Finished generating static gesture!")

    def generate_static_gesture_from_sample(self,
                                            label: str,
                                            hand: str,
                                            sample_values: list[str],
                                            file_type: str) -> None:
        """
        Generates a static gesture from the given data in WACH format as list.
        :param label:
        :param hand:
        :param sample_values:
        :param file_type:
        :return:
        """
        print("Generating static gesture ...")

        # Assert arguments
        if self.blender_path is None:
            print("Blender must be installed and in path!")
            return

        self.__read_sample(label, hand, sample_values)
        self.__export_as(file_type)

        print("Finished generating static gesture!")

    def __read_from_file(self, file_path: str) -> None:
        """
        Reads a file that contains one or more samples in WACH format for a gesture.
        :param file_path: File Path. (E.g.:
        https://github.com/serious-games-darmstadt/dataglove_manus-prime-x_handshapes/blob/main/wach_format/1/a_20220503.txt)
        :return: None
        """
        # Reset attributes
        self.__reset()

        # Save input file name TODO: make it method for base class and use in static and dynamic
        norm_input_file_path = os.path.abspath(file_path)
        input_file_type = norm_input_file_path[norm_input_file_path.rfind('.') + 1:]
        if input_file_type not in self.SUPPORTED_IN_FILE_TYPES:
            print("Input file type not supported!")
            return
        self.input_file_name = norm_input_file_path[norm_input_file_path.rfind(os.sep) + 1:(-1 * (
                len(input_file_type) + 1))]

        # Get samples from file
        with open(norm_input_file_path, 'r') as f:
            content = f.readlines()
            while content[-1] == '\n':  # Remove trailing new lines
                del content[-1]

        # Extract label and hand type from file
        self.label = content[0].rstrip('\n')
        self.hand = content[1].rstrip('\n')

        # Extract all data samples from file
        start_idx = 3  # skip label, hand type and first newline
        number_of_features = 20  # length of a data sample in WACH format
        while start_idx < len(content):
            end_idx = start_idx + number_of_features
            self.data_samples.append([line.rstrip('\n') for line in content[start_idx:end_idx]])
            start_idx = end_idx + 1

    def __read_sample(self, label: str, hand: str, sample_values: list[str]) -> None:
        """
        Reads data sample in WACH format.
        :param label: Name of the performed gesture.
        :param hand: 'Left' or 'Right' hand.
        :param sample_values: Data sample in WACH format.
        :return: None
        """
        # Reset attributes
        self.__reset()

        self.label = label
        self.hand = hand
        self.data_samples.append(sample_values)
        self.input_file_name = label

    def __export_as(self, export_file_type: str) -> None:
        """
        Runs the blender script and exports result as file.
        :param export_file_type: Desired output file type.
        :return: None
        """
        # Run script for each sample
        for idx, sample in enumerate(self.data_samples):
            self.__create_blender_script_with_values(export_file_type, sample, idx)
            self.__run_blender_script()
            self.__reset_blender_script_for_values(export_file_type, sample, idx)

    def __reset(self) -> None:
        """
        Resets attributes so that new sample(s) can be read.
        :return: None
        """
        self.label = ""
        self.hand = ""
        self.data_samples = []
        self.input_file_name = R""

    def __create_blender_script_with_values(self,
                                            export_file_type: str,
                                            sample_values: list[str],
                                            sample_number: int):

        # Replace label variable in blender_script_static.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace("LABEL = ''", f"LABEL = '{self.label}'").rstrip())

        # Replace hand variable in blender_script_static.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace("HAND = ''", f"HAND = '{self.hand}'").rstrip())

        # Replace sample_values variable in blender_script_static.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace("sample_values = []", f"sample_values = {str(sample_values)}").rstrip())

        # Replace export_file_type variable in blender_script_static.py
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(
                "EXPORT_FILE_TYPE = ''", f"EXPORT_FILE_TYPE = '{export_file_type}'").rstrip())

        # Replace output path
        for output_file_type in self.SUPPORTED_OUT_FILE_TYPES:
            out_str = f"{output_file_type.upper()}_PATH_STR"
            old_output_path = f"{out_str} = ''"
            new_value = os.path.join(self.output_dir,
                                     f"{self.input_file_name}_{self.hand}_{sample_number}_{output_file_type}.{output_file_type}")
            new_output_path = f"{out_str} = R'{new_value}'"
            for line in fileinput.input(self.blender_script_path, inplace=True):
                print(line.replace(old_output_path, new_output_path).rstrip())

    def __reset_blender_script_for_values(self,
                                          export_file_type: str,
                                          sample_values: list[str],
                                          sample_number: int) -> None:

        # Reset each change done in __create_blender_script_with_values()
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(f"LABEL = '{self.label}'", "LABEL = ''").rstrip())
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(f"HAND = '{self.hand}'", "HAND = ''").rstrip())
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(f"sample_values = {str(sample_values)}", "sample_values = []").rstrip())
        for line in fileinput.input(self.blender_script_path, inplace=True):
            print(line.replace(
                f"EXPORT_FILE_TYPE = '{export_file_type}'", "EXPORT_FILE_TYPE = ''").rstrip())

        for output_file_type in self.SUPPORTED_OUT_FILE_TYPES:
            out_str = f"{output_file_type.upper()}_PATH_STR"
            old_output_path = f"{out_str} = ''"
            new_value = os.path.join(self.output_dir,
                                     f"{self.input_file_name}_{self.hand}_{sample_number}_{output_file_type}.{output_file_type}")
            new_output_path = f"{out_str} = R'{new_value}'"
            for line in fileinput.input(self.blender_script_path, inplace=True):
                print(line.replace(new_output_path, old_output_path).rstrip())

    def __run_blender_script(self):
        # Build command line arguments
        args = [self.blender_path, "--background", "--python", self.blender_script_path]

        # Run blender process with script
        subprocess.run(args)
