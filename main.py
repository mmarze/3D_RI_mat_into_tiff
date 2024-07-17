import hdf5storage
from PIL import Image
import numpy as np


def read_mat_file(filepath, z):
    """This function read the measurement data from a .mat file. The data must 
contain a 'n_rec' variable.

    Parameters
    ----------
    filepath : str
        Data to transform.
    z : [int]
        Selected depths across Z (propagation) axis. Format: [z_min, z_max].

    Returns
    -------
    data_out : numpy.ndarray
        Loaded data."""
    data_out = hdf5storage.loadmat(filepath)['n_rec'][:, :, z[0]:z[1]]
    print("Data has been succesfully red from .mat file")
    return data_out


def image_data_normalization(data):
    """This function normalize the measurement data to numpy.uint8 format and 
value range from 0 to 255.

    Parameters
    ----------
    data : numpy.ndarray
        Data to transform.

    Returns
    -------
    data : numpy.ndarray
        Transformed data."""
    # 0-1 normalization
    vol_min = np.min(data)
    vol_max = np.max(data)
    data = (data - vol_min) / (vol_max - vol_min)
    print("Pixel values normalized [0; 1] succesfully")

    # zmiana wartosci - z RI na intensywnosc obrazu!!!!
    levels = 256
    data = levels * data
    print("Pixel values normalized [0; 255] succesfully")
    data = data.astype(np.uint8)
    print("Pixel values converted to uint8 successfully")
    return data


def save_to_3D_tiff(data, filepath='my_tiff.tiff'):
    """This function saves a data from 3D numpy.ndarray into a multi-page tiff 
file.

    Parameters
    ----------
    data : numpy.ndarray
        Data to save.
    filepath : str
        Filepath for a .tiff file. Default: "my_tiff.tiff"

    Returns
    -------
    None"""
    frames = []
    for i in range(np.shape(data)[2]):
        # Convert data to PIL Image
        img = Image.fromarray(data[:, :, i])
        frames.append(img)

    # Save the images as a multi-page TIFF
    frames[0].save(filepath, save_all=True, append_images=frames[1:])
    print("Multi-page TIFF saved successfully")


def mat_to_tiff(filepath_mat, filepath_tiff, z):
    """This function read a .mat file with 3D RI data, normalize it, and save 
as a multi-page tiff image.
    
    Parameters
    ----------
    filepath_mat : str
        Filepath to the .mat file with measurement data.
    filepath_tiff : str
        Filepath to a tiff file.
    z : [int]
        Selected depths across Z (propagation) axis. Format: [z_min, z_max].

    Returns
    -------
    data_temp : numpy.ndarray of np.uint8
        Normalized intensity data [0; 255]."""
    data_temp = read_mat_file(filepath_mat, z)
    data_temp = image_data_normalization(data_temp)
    save_to_3D_tiff(data_temp, filepath_tiff)
    return data_temp


def main():
    my_filename_mat = r"Desktop\DI_light.mat"
    my_filename_tiff = r"Desktop\my_file_new.tiff"
    # z - selected images across Z axis
    z = [600, 1000]
    my_data = mat_to_tiff(my_filename_mat, my_filename_tiff, z)
    return my_data
    

if __name__ == '__main__':
   my_data = main()
   
