from PIL import Image
import os

BASE_PATH = "blue jay"
OUTPUT_PATH = "outputs"

def compose(img1, img2):
    if isinstance(img1, str):
        base = Image.open(img1).convert("RGBA")
    else:
        base = img1
    overlay = Image.open(img2).convert("RGBA")
    return Image.alpha_composite(base, overlay)

def combine_list(layers):
    if len(layers) == 0:
        return None
    elif len(layers) == 1:
        return Image.open(layers[0]).convert("RGBA")
    
    cur_comp = compose(layers[0], layers[1])
    for i in range(2, len(layers)):
        cur_comp = compose(cur_comp, layers[i])

    return cur_comp

def save_image(img, combo_list):
    img.save(f"{OUTPUT_PATH}/{"_".join(combo_list)}.png")

def backtrack(categories, cur_combo_img, cur_combo_list, i):  
    for filename in os.listdir(f"{BASE_PATH}/{categories[i]}"):
        cur_combo_list.append(filename)
        new_combo_img = compose(cur_combo_img, f"{BASE_PATH}/{categories[i]}/{filename}")
        if i < len(categories) - 1:
            backtrack(categories, new_combo_img, cur_combo_list, i+1)
        else:
            save_image(new_combo_img, cur_combo_list)
        cur_combo_list.pop()
            


if __name__ == "__main__":
    layers = [
        "blue jay/main bird/front.png",
        "blue jay/main bird/lineart.png",
        "blue jay/main bird/feathers.png",
    ]
    base = combine_list(layers)
    categories = [
        "base",
        "accent",
        "accessory"
    ]
    backtrack(categories, base, ["base"], 1)