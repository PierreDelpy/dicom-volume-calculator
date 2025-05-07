import pydicom
import numpy as np
from config import THRESHOLD

def process_dicom(file, threshold=THRESHOLD):
    # Read DICOM file
    dataset = pydicom.dcmread(file)
    #print(dataset)

    pixel_data = dataset.pixel_array.astype(np.float32) # task 2.C:) Extraction of pixel data from the DICOM
    
    pixel_data_norm = (pixel_data - np.min(pixel_data)) / (np.max(pixel_data) - np.min(pixel_data)) # task 2.D:) Normalize the pixel data to a range of [0, 1].
    pixel_result = {"pixel_shape": pixel_data.shape, "pixel_dtype": str(pixel_data.dtype)}
    
    spacing = dataset.PixelSpacing  # [row_spacing, col_spacing]
    thickness = dataset.SliceThickness  # slice thickness in mm

    
    mask = pixel_data_norm > threshold # task 2.E:)Use the threshold value specified in the web server’s config file (default to 0.5 if not provided)
    voxel_volume = float(spacing[0]) * float(spacing[1]) * float(thickness)
    num_pixels_above_threshold = int(np.sum(mask))
    volume = num_pixels_above_threshold * voxel_volume


    return {"extracted_pixel_data": pixel_result, "volume": round(volume, 3), "pixels_above_threshold": num_pixels_above_threshold}
