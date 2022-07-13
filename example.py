from visualization import viz
import os


def static_gesture_visualization_example() -> None:
    """
    Static gesture visualization example.
        1. Either visualize data by WACH txt files (3 gestures each) or provide user defined values in a list.
    """

    # Create static visualizer object
    static_viz = viz.StaticDataVisualizer()  # default output path (./output/static)
    # static_viz = viz.StaticDataVisualizer(R"path\to\output\dir")  # user defined output path

    # Generate a single sample (label, hand, values, export_file_type)
    # User defined values as list
    # sample_values = [
    #     '1.0',  # thumb spread
    #     '0.0',  # index spread
    #     '0.0',  # middle spread
    #     '0.0',  # ring spread
    #     '0.0',  # pinky spread
    #     '0.69',  # thumb stretch cmc
    #     '1.0',  # thumb stretch mcp
    #     '1.0',  # thumb stretch ip
    #     '1.0',  # index stretch mcp
    #     '1.0',  # index stretch pip
    #     '1.0',  # index stretch dip
    #     '1.0',  # middle stretch mcp
    #     '1.0',  # middle stretch pip
    #     '1.0',  # middle stretch dip
    #     '1.0',  # ring stretch mcp
    #     '1.0',  # ring stretch pip
    #     '1.0',  # ring stretch dip
    #     '1.0',  # pinky stretch mcp
    #     '1.0',  # pinky stretch pip
    #     '1.0'   # pinky stretch dip
    # ]
    # static_viz.generate_static_gesture_from_sample('faust', 'Left', sample_values, 'stl')

    # Generate multiple samples from file (file_path, export_file_type)
    static_viz = viz.StaticDataVisualizer()
    # static_viz = viz.StaticDataVisualizer(R"./src")
    static_viz.generate_static_gesture_from_file(R"./example_static.txt", 'stl')


def dynamic_gesture_visualization_example() -> None:
    """
    Dynamic gesture visualization example.
        1. Choose gesture label, i.e. z1, z2, j1, j2 ... (z and j only dynamic, but all can be dynamically visualized).
        2. Generate gesture by exporting or directly opening blender by providing processed json files.
    """

    # Create dynamic visualizer object
    dynamic_viz = viz.DynamicDataVisualizer()  # default output path (./output/dynamic)
    # dynamic_viz = viz.DynamicDataVisualizer(R"path\to\output\dir")  # user defined output path

    # Processed data path and specific label
    input_json_path = os.path.abspath(R"./example_dynamic.json")

    # This might take a few seconds since the processed_data json files are scanned for the right gesture.
    dynamic_viz.generate_dynamic_gesture(input_json_path, export=True)
    # dynamic_viz.generate_dynamic_gesture(input_json_path, export=False)


def main():
    static_gesture_visualization_example()
    dynamic_gesture_visualization_example()


if __name__ == '__main__':
    main()
