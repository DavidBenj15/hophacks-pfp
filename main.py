"""
main.py

A utility for programmatically composing and exporting layered bird PFP images using the Python Imaging Library (PIL).
This module is intended to generate variations of a base bird image by overlaying different image assets such as
backgrounds, accessories, and other elements.

Important Variables:
- BASE_PATH: where each layer is stored. Assumes the following file structure:
    BASE_PATH/<category_name>/<category_name> <digit>.png
    BASE_PATH/main bird/*.png
"""
from PIL import Image
import os

BASE_PATH = "blue jay" # Where layers are stored.
OUTPUT_PATH = "pfps" # Where PFP combinations are outputted.

def compose(img1, img2):
    """
    Composes two images.
    Args:
        img1 (None | str | Image): base image.
        img2 (str): overlay image.
    Returns:
        Image: the composite of img2 on top of img1.
    """
    overlay = Image.open(img2).convert("RGBA")
    if img1 is None:
        return overlay
    elif isinstance(img1, str):
        base = Image.open(img1).convert("RGBA")
    else:
        base = img1
    return Image.alpha_composite(base, overlay)

def combine_list(layers):
    """
    Sequentially combines all image paths provided in "layers",
    with the last element being on top.
    Args:
        layers (List[str]): list of files to combine.
    Returns:
        Image: combined layers.
    """
    if len(layers) == 0:
        return None
    elif len(layers) == 1:
        return Image.open(layers[0]).convert("RGBA")
    
    cur_comp = compose(layers[0], layers[1])
    for i in range(2, len(layers)):
        cur_comp = compose(cur_comp, layers[i])

    return cur_comp

def save_image(img, combo_list):
    """
    Saves image w/ a programatically generated name. More specifically as:

    <stages>_<body>_<main bird COMPOSED>_<accent>_<accessory>_<object>.png

    Each parameter in the file name above will be a digit corresponding to the file name;
    e.g., "1" for "stage 1.png", or "0" if that category is not included in the final image.

    Args:
        img (Image): image to save.
        combo_list (List[str]): list of file names (or "0").
    """
    # Each item in "combo_list" will be named either "0" (no item for that category)
    # or <category> <digit>.png. The line below joins the digit of each item.
    indexed_name = "_".join([name.removesuffix(".png")[-1] for name in combo_list])
    img.save(f"{OUTPUT_PATH}/{indexed_name}.png")

def make_mainbird():
    """
    Compose and save the main bird image.
    """
    layers = []
    for filename in ["front.png", "lineart.png", "feathers.png"]:
        layers.append(f"{BASE_PATH}/main bird/{filename}")

    img = combine_list(layers)
    output_dir = f"{BASE_PATH}/main bird COMPOSED"
    os.makedirs(output_dir, exist_ok=True)
    img.save(f"{output_dir}/main 1.png")

def dfs(categories, cur_combo_img, cur_combo_list, i):
    """
    Use backtracking to generate and save every possible combination
    of (1 or 0 items from each category).
    
    Args:
        categories (List[str]): list of directory names for each category.
        cur_combo_img (Image): the current composition that our backtracking has produced.
        cur_combo_list (List[str]): a list of each item included in cur_combo_img.
        i (int): used to index the current category we are selecting from.
    """
    # For certain categories, "no item selected" should be an option.
    if categories[i] in {"stages", "accent", "accessory", "object"}:
        cur_combo_list.append("0") # Indicate no item selected for this category.
        if i < len(categories) - 1:
            dfs(categories, cur_combo_img, cur_combo_list, i+1)
        else:
            save_image(cur_combo_img, cur_combo_list)
        cur_combo_list.pop() # Backtrack

    for filename in os.listdir(f"{BASE_PATH}/{categories[i]}"):
        cur_combo_list.append(filename)
        new_combo_img = compose(cur_combo_img, f"{BASE_PATH}/{categories[i]}/{filename}")
        if i < len(categories) - 1:
            dfs(categories, new_combo_img, cur_combo_list, i+1)
        else:
            save_image(new_combo_img, cur_combo_list)
        cur_combo_list.pop() # Backtrack
            

if __name__ == "__main__":
    make_mainbird()
    categories = [
        "stages",
        "body",
        "main bird COMPOSED",
        "accent",
        "accessory",
        "object",
    ]
    dfs(categories, None, [], 0)
