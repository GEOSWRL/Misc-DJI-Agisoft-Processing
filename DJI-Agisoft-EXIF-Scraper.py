# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:56:38 2020

@author: Andrew Mullen
"""
import os
import pandas as pd
import exiftool

"""

This program uses pyexiftool: http://smarnach.github.io/pyexiftool/ , which can be installed by running "pip install pyexiftool"
in the IPython Console

Since pyexiftool is a Python wrapper for the Exiftool software (command line application written in Perl), we also need to install
Exiftool. Download the application (https://exiftool.org/), and set the EXIFTOOL_PATH variable in this file to the path to your
exiftool installation.

"""
#set path to exiftool application
EXIFTOOL_PATH = ''

#set input/output paths
image_directory = ''
output_directory = ''

def read_EXIF(path_to_images, path_to_output):
    
    """
    Reads EXIF data from DJI images and creates a text file with GPS fields for use in Agisoft

    Parameters
    ----------
    path_to_images : string
        path to DJI images
        
    path_to_output : string
        path to save csv file to
    
    Returns
    -------
    result : string
        path to .csv file
    """
    #create empty dataframe with column headings
    df = pd.DataFrame(columns = ['Image ID', 'GPSLatitude', 'GPSLongitude', 'GPSAltitude', 'Pitch', 'Roll', 'Yaw'])
    
    with exiftool.ExifTool(EXIFTOOL_PATH) as et:
        for filename in os.listdir(path_to_images):
            if (filename.endswith('.DNG') or filename.endswith('.JPG')):
                
                print(filename)
                
                #get metadata
                metadata = et.get_metadata_batch([path_to_images + filename])[0]  
                GPSLongitude = metadata['Composite:GPSLongitude']
                GPSLatitude = metadata['Composite:GPSLatitude']
                GPSAltitude = metadata['Composite:GPSAltitude']
                Pitch = metadata['MakerNotes:CameraPitch'] + 90
                
                if (metadata['MakerNotes:CameraYaw']>=0):
                    Yaw = metadata['MakerNotes:CameraYaw']
                else:
                    Yaw = 360 + metadata['MakerNotes:CameraYaw']
                Roll = metadata['MakerNotes:CameraRoll']            
                
                #add items to dataframe
                df = df.append(pd.Series([filename, GPSLatitude, GPSLongitude, GPSAltitude,
                                          Pitch, Roll, Yaw], index=df.columns), ignore_index = True)

    df.set_index('Image ID', inplace = True)
    
    #save to .csv file
    df.to_csv(path_to_output + 'EXIF.csv')
                            
    return (path_to_output + 'EXIF.csv')

read_EXIF(image_directory, output_directory)
