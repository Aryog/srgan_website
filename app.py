from flask import Flask, render_template, request
import torch
import os
from PIL import Image
import numpy as np
from generator import Generator
from datetime import datetime, timedelta
app = Flask(__name__)

def preprocess_input(image_path):
    # Load the input image
    input_image = Image.open(image_path).convert("RGB")
    input_image = np.array(input_image) / 127.5 - 1.0
    input_image = input_image.transpose(2, 0, 1).astype(np.float32)
    return torch.tensor(input_image).unsqueeze(0)

def test_single_image(generator_path, input_image_path, output_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the generator model
    generator = Generator()          #for ours
    state_dict = torch.load(generator_path, map_location='cpu')
    if 'module.' in list(state_dict.keys())[0]:
        state_dict = {k[7:]: v for k, v in state_dict.items()}
    
    generator.load_state_dict(state_dict)
    generator.eval()

    # Preprocess the input image
    input_image = preprocess_input(input_image_path).to(device)

    # Perform inference
    with torch.no_grad():
        output = generator(input_image)
        output = output[0].cpu().numpy()
        output = (output + 1.0) / 2.0
        print(f'This is output shape before transpose: {output.shape}')
        # Add this line to check the content of the output array
        print(f'This is output content before transpose: {output}')
        output = output.transpose(1, 2, 0)
        # output = output.transpose(0, 2, 3, 1)
        result = Image.fromarray((output * 255.0).astype(np.uint8)) # for ours
        # result = Image.fromarray((output[0] * 255.0).astype(np.uint8))
        result.save(output_path)

if __name__ == "__main__":
    # Specify the paths and parameters
    # generator_path = "./model/pre_trained_model_064.pt"
    generator_path = "MedSRGAN_gene_032.pt"

    # Test the model with a single image

@app.route('/', methods=['GET'])
def hello_word():
    return render_template('index.html')

# Function to clean up files older than a specified threshold to prevent container from growing
def clean_up_files(folder, hours_threshold):
    now = datetime.now()
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - modified_time > timedelta(hours=hours_threshold):
                os.remove(file_path)

@app.route('/', methods=['GET', 'POST'])
def predict():
    image_uploaded = False
    if request.method == 'POST':
        imagefile = request.files.get('imagefile')
        if imagefile and imagefile.filename:
            image_path = "./static/input/" + imagefile.filename
            imagefile.save(image_path)

            output_path = "./static/enhanced/" + imagefile.filename

            test_single_image(generator_path, image_path, output_path)
            print(output_path)

            # Clean up files older than 3 hours in the input and enhanced folders
            clean_up_files("./static/input/", 1)
            clean_up_files("./static/enhanced/", 1)

            image_uploaded = True
            return render_template('index.html', prediction=output_path, inputFile=image_path, image_uploaded=image_uploaded)

    return render_template('index.html', image_uploaded=image_uploaded)




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000,debug=False)