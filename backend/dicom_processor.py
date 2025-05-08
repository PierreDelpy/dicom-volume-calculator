import pydicom
import numpy as np
from config import THRESHOLD

def process_dicom(file, threshold=THRESHOLD):
    # Read DICOM file
    dataset = pydicom.dcmread(file)
    # print(dataset)

    pixel_data = dataset.pixel_array.astype(np.float32) # task 2.C:) Extraction of pixel data from the DICOM
    # normalize
    pixel_data_norm = (pixel_data-np.min(pixel_data))/(np.max(pixel_data)-np.min(pixel_data)) # task 2.D:) Normalize the pixel data to a range of [0, 1].
    # provide result for 2.D
    pixel_result = {"pixel_shape": pixel_data.shape, "pixel_dtype": str(pixel_data.dtype)}
    pixel_data_binary = pixel_data_norm > threshold # task 2.E:)Use the threshold value specified in the web server’s config file (default to 0.5 if not provided)
    num_pixels_above_threshold = int(np.sum(pixel_data_binary))

    # generate 3D relevant information (x * y * z)
    pixelSpacing = dataset.PixelSpacing  # 2D information = x * y
    sliceThickness = dataset.SliceThickness  # slice thickness in mm = z information
    # generate voxel_volume = 3D Pixel = x * y * z
    voxel_volume = float(pixelSpacing[0]) * float(pixelSpacing[1]) * float(sliceThickness)
    # generate volume of interest = keep only relevant amount of volume 
    volume = num_pixels_above_threshold * voxel_volume


    return {"extracted_pixel_data": pixel_result, "pixels_above_threshold": num_pixels_above_threshold, "voxel_volume": voxel_volume, "volume": round(volume, 3)}

# for debugging
if __name__ == "__main__":
    from pathlib import Path
    test_file = Path("./1-101.dcm")
    volume = process_dicom(test_file)
    print(f"Calculated volume: {volume:.3f} mm³")