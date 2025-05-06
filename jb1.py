#!/usr/bin/env python

# Purpose : Jodrell Bank Demo Program Number 1. 

# Ensure that environment variable PYTHONUNBUFFERED=yes
# This allows STDOUT and STDERR to both be logged in cronological order

import sys                       # platform, args, run tools
import os                        # platform, args, run tools
                                                    
import argparse                  # For parsing command line
import datetime                  # For date/time processing

import inspect                   # For listing modules
import importlib as implib       # For listing modules

import casacore.tables
import ducc0
import numpy
import math
import scipy.signal.windows

import matplotlib as mpl
from matplotlib import pylab
from matplotlib import pyplot

from astropy.io import fits

#########################################################################
# Command Line Parameters Class
#########################################################################

class Jb1CP():

    def jb1_cp(self, jb1_cmd_line):        

        description = ("Jodrell Bank Demo Program Number 1")
        parser = argparse.ArgumentParser(description=description,
                                         formatter_class=argparse.RawTextHelpFormatter)

        help_text = ("Input table name")      
        parser.add_argument("input_table_name",
                            metavar="input_table_name",
                            #type=string,
                            help=help_text)

        self.spec_name = "SPECTRAL_WINDOW"
        help_text = ("Spec name " +
                     "(DEFAULT=SPECTRAL_WINDOW)")        
        parser.add_argument("-s", "--spec_name",
                          default=self.spec_name,
                          help=help_text,
                          action="store",
                          #type="string",                          
                          dest="spec_name")
        
        self.output_file_name = "jb1_output.png"
        help_text = ("Output directory " +
                     "(DEFAULT=jb1_output.png)")        
        parser.add_argument("-o", "--output_file_name",
                          default=self.output_file_name,
                          help=help_text,
                          action="store",
                          #type="string",                          
                          dest="output_file_name")
        
        self.output_directory = os.getcwd()
        help_text = ("Output directory " +
                     "(DEFAULT=CURRENT)")        
        parser.add_argument("-d", "--output_directory",
                          default=self.output_directory,
                          help=help_text,
                          action="store",
                          #type="string",                          
                          dest="output_directory")

        self.num_iterations = 600
        help_text = ("Output directory " +
                     "(DEFAULT=600)")        
        parser.add_argument("-it", "--num_iterations",
                          default=self.num_iterations,
                          help=help_text,
                          action="store",
                          #type="string",                          
                          dest="num_iterations")

        def resolution_range(x):
            try:
                x = int(x)
            except ValueError:
                raise argparse.ArgumentTypeError("%r not an integer literal" % (x,))
            
            if (x < 30):
                raise argparse.ArgumentTypeError("%r Minimum 30"%(x,))
            if (x > 300):
                raise argparse.ArgumentTypeError("%r Maximum 300"%(x,))
            return x

        
        self.resolution = 100
        help_text = ("Resolution of output graphics file in DPI " +
                     "(DEFAULT=100dpi, RANGE=30-300dpi)")        
        parser.add_argument("-r", "--resolution",
                            type=resolution_range,
                            #type=int,
                            default=self.resolution,
                            #choices=range(30, 300),
                            metavar="RESOLUTION [30-300]",
                            help=help_text,
                            action="store",                 
                            dest="resolution")
        
        help_text = ("List Python Modules imported to this program " +
                     "(DEFAULT=NO)")        
        parser.add_argument("-lpm", "--list_python_modules",
                          default=False,
                          help=help_text,
                          action="store_true",
                          dest="list_python_modules")

        help_text = ("Display processing messages to STDOUT " +
                     "(DEFAULT=NO)")        
        parser.add_argument("-v", "--verbose",
                          default=False,
                          help=help_text,
                          action="store_true",
                          dest="verbose")

        help_text = ("Run program in test mode " +
                     "(DEFAULT=NO)")        
        parser.add_argument("-t", "--test_mode",
                          default=False,
                          help=help_text,
                          action="store_true",
                          dest="test_mode")

        self.args = parser.parse_args(jb1_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("JB1 : jb1_cmd_line = {}\n".format(str(jb1_cmd_line)))

        self.args.output_directory = os.path.abspath(self.args.output_directory.strip()) 

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class Jb1():

    def jb1(self, jb1_cmd_line):
          
# Start time

        self.start_time = datetime.datetime.today()

# Parse input parameters from cmd line

        jb1_cp1     = Jb1CP()
        jb1_cp1_ret = jb1_cp1.jb1_cp(jb1_cmd_line)        

        self.jb1_cmd_line = jb1_cmd_line
        if (len(self.jb1_cmd_line) == 0):
            self.jb1_cmd_line = " " 

        if (jb1_cp1_ret):
            return(jb1_cp1_ret)

        self.spec_name           = jb1_cp1.args.spec_name
        self.output_file_name    = jb1_cp1.args.output_file_name
        self.output_directory    = jb1_cp1.args.output_directory
        self.num_iterations      = int(jb1_cp1.args.num_iterations)
        self.resolution          = int(jb1_cp1.args.resolution)
        self.list_python_modules = jb1_cp1.args.list_python_modules
        self.verbose             = jb1_cp1.args.verbose   
        self.test_mode           = jb1_cp1.args.test_mode                
        self.input_table_name    = jb1_cp1.args.input_table_name

        if (self.test_mode):
            self.timestamp = "Test Mode Date/Time Stamp"
            if (self.verbose):                
                sys.stdout.write("JB1 : Running in test mode\n")
                sys.stdout.write("JB1 : sys.version = {}\n".format(str(sys.version).strip()))                     
        else:
            self.timestamp = datetime.datetime.now()#.strftime("%Y-%m-%dT%H:%M:%S")
            if (self.verbose):
                sys.stdout.write("JB1 : Program started = {}\n".format(str(self.start_time.astimezone().isoformat(sep="T")).strip()))
                sys.stdout.write("JB1 : self.timestamp  = {}\n".format(str(self.timestamp.astimezone().isoformat(sep="T", timespec="seconds")).strip()))   
                sys.stdout.write("JB1 : sys.version     = {}\n".format(str(sys.version).strip()))
                
        if (os.path.isdir(self.output_directory)):
            pass
        else:
            if (self.verbose):                       
                sys.stderr.write("JB1 : ERROR : \nUnrecognized output directory : {}\n".format(str(self.output_directory).strip()))  
                sys.stderr.write("JB1 : ERROR : Defaulting to current directory\n\n")
            self.output_directory = os.getcwd()
            
        self.output_directory = os.path.abspath(self.output_directory)

        if (self.verbose):
            sys.stdout.write("JB1 : sys.version              =  {}\n".format(str(sys.version).strip()))     
            sys.stdout.write("JB1 : self.spec_name           =  {}\n".format(str(self.spec_name).strip()))     
            sys.stdout.write("JB1 : self.output_file_name    =  {}\n".format(str(self.output_file_name).strip()))
            sys.stdout.write("JB1 : self.output_directory    =  {}\n".format(str(self.output_directory).strip()))
            sys.stdout.write("JB1 : self.num_iterations      =  {}\n".format(str(self.num_iterations).strip()))
            sys.stdout.write("JB1 : self.resolution          =  {}\n".format(str(self.resolution).strip()))
            sys.stdout.write("JB1 : self.list_python_modules =  {}\n".format(str(self.list_python_modules).strip()))
            sys.stdout.write("JB1 : self.verbose             =  {}\n".format(str(self.verbose).strip()))
            sys.stdout.write("JB1 : self.test_mode           =  {}\n".format(str(self.test_mode).strip()))
            sys.stdout.write("JB1 : self.input_table_name    =  {}\n".format(str(self.input_table_name).strip()))   

# List imported Python modules

        if (self.list_python_modules) :
            if (__name__ == "__main__"):
                self.import_list = implib.import_module("jb1")
            if (self.verbose):
                for self.module_list in inspect.getmembers(self.import_list, inspect.ismodule ):
                    sys.stdout.write("JB1 : Module imported : {}\n".format(str(self.module_list[0])))
                    sys.stdout.write("JB1 : Module imported : {}\n".format(str(self.module_list[1]))) # Shows paths

# Set Numpy Array Printing Options

        numpy.set_printoptions(precision=3)   # Limit Numpy printing precision to 3dp
        numpy.set_printoptions(suppress=True) # Suppress Numpy scientific notation for small numbers

# Call functions

        jb1_f11_ret = self.read_input_data()
        if (jb1_f11_ret):
            return(jb1_f11_ret)

        jb1_f11_ret = self.make_basic_image()
        if (jb1_f11_ret):
            return(jb1_f11_ret)

        jb1_f11_ret = self.output_basic_image_figure()
        if (jb1_f11_ret):
            return(jb1_f11_ret)
        
        jb1_f11_ret = self.output_basic_image_fits()
        if (jb1_f11_ret):
            return(jb1_f11_ret)

        jb1_f11_ret = self.make_cleaned_image()
        if (jb1_f11_ret):
            return(jb1_f11_ret)

        jb1_f11_ret = self.output_cleaned_image_figure()
        if (jb1_f11_ret):
            return(jb1_f11_ret)

        jb1_f11_ret = self.output_cleaned_image_fits()
        if (jb1_f11_ret):
            return(jb1_f11_ret)
        
# End program

        self.end_time = datetime.datetime.today()
        self.run_time = self.end_time - self.start_time 

        if (self.verbose):
            if (self.test_mode):
                pass
            else:
                sys.stdout.write("JB1 : Program ended : {}\n".format(str(self.end_time.astimezone().isoformat(sep="T"))))
                sys.stdout.write("JB1 : Run time      : {}\n".format(str(self.run_time)))

        if (self.verbose):                       
            sys.stdout.write("JB1 : Program completed normally\n")
            
        return(0)

# Define functions

#------------------------------------------------------------------------------

    def read_input_data(self):
        if (self.verbose):
           sys.stdout.write("JB1 : read_input_data ACTIVATED\n")

        #self.tbl_name  = "pipeline_problem_data.ms"
        #self.spec_name = "pipeline_problem_data.ms/SPECTRAL_WINDOW"

        self.spec_name_full = os.path.normpath(self.input_table_name + "/" + self.spec_name)
        self.spec_name_full = os.path.abspath(self.spec_name_full)

        if (self.verbose):
            sys.stdout.write("JB1 : self.input_table_name = " + str(self.input_table_name) + "\n")
            sys.stdout.write("JB1 : self.spec_name_full   = " + str(self.spec_name_full)   + "\n")
        
        try:
            self.tbl  = casacore.tables.table(self.input_table_name)
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to read table " + str(self.input_table_name) + "\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)
        
        try:
            self.spec = casacore.tables.table(self.spec_name_full)
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to read spectral window " + str(self.spec_name) + "\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)

# Display input data

        if (self.verbose):
            sys.stdout.write("JB1 : self.tbl  = " + str(self.tbl)  + "\n")
            sys.stdout.write("JB1 : self.spec = " + str(self.spec)  + "\n")
        
# Set up filter to remove auto-correlations from the data

        try:
            self.autocorr_filter = self.tbl.getcol("UVW")[:,0] == 0
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to obtain auto-correlations from " + str(self.tbl_name) + "\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)

        return(0)

#------------------------------------------------------------------------------

    def make_basic_image(self):
        if (self.verbose):
           sys.stdout.write("JB1 : make_basic_image ACTIVATED\n")
        
# Create an image using the wgridder from DUCC

        try:
            self.vis = numpy.sum(self.tbl.getcol("DATA"), axis=2)
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to obtain table data  from " + str(self.tbl_name) + "\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)

        self.fov_size = 2.2
        self.img_size = 1024
        self.pixsize  = 2 * math.pi * self.fov_size / 360 / self.img_size

        try:
            self.basic_image = ducc0.wgridder.ms2dirty(
                self.tbl.getcol("UVW")[~self.autocorr_filter],
                self.spec.getcol("CHAN_FREQ")[0],
                self.vis[~self.autocorr_filter],
                npix_x=self.img_size,
                npix_y=self.img_size,
                pixsize_x=self.pixsize,
                pixsize_y=self.pixsize,
                epsilon=1.0e-3,
                do_wstacking=True,
            )
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to generate basic image\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)

        self.basic_image = self.basic_image.T # Transpose Image
        
# Display basic image attributes

        if (self.verbose):
            sys.stdout.write("JB1 : self.basic_image.dtype = " + str(self.basic_image.dtype)  + "\n")
            sys.stdout.write("JB1 : self.basic_image.shape = " + str(self.basic_image.shape)  + "\n")
            sys.stdout.write("JB1 : self.basic_image.ndim  = " + str(self.basic_image.ndim)   + "\n")
            sys.stdout.write("JB1 : self.basic_image.size  = " + str(self.basic_image.size)   + "\n")

        return(0)
            
#------------------------------------------------------------------------------

    def output_basic_image_figure(self):
        if (self.verbose):
           sys.stdout.write("JB1 : output_basic_image_figure ACTIVATED\n")

# Make basic image output graphic file name

        self.basic_image_output_graphic_file_name = self.output_file_name.replace(".png", "_basic.png")
        self.basic_image_output_graphic_file_name = os.path.normpath(self.output_directory + "/" + self.basic_image_output_graphic_file_name)
        self.basic_image_output_graphic_file_name = os.path.abspath(self.basic_image_output_graphic_file_name)
        if (self.verbose):
            sys.stdout.write("JB1 : self.basic_image_output_graphic_file_name = " + str(self.basic_image_output_graphic_file_name) + "\n")
           
# Setup figure

        self.fig_basic = mpl.pyplot.figure(1, figsize=(8.27, 11.69)) # A4 size        
        self.fig_basic.suptitle("JB1 - Basic Image\n{}".format(str(self.timestamp.astimezone().isoformat(sep="T", timespec="seconds")).strip())) 
        self.fig_basic.text(0.05, 0.93, "Output file name = {}".format(self.basic_image_output_graphic_file_name))
        self.fig_basic.text(0.05, 0.91, "Input file name = {}".format(self.spec_name_full))
        self.fig_basic.text(0.05, 0.89, "Graphical file resoloution (dpi) = {:d}".format(self.resolution))
        self.fig_basic.text(0.05, 0.87, "FOV size = {:4.2f}".format(self.fov_size))
        self.fig_basic.text(0.05, 0.85, "Pixel size = {:6.3e}".format(self.pixsize))
        
        self.fig_basic.subplots_adjust(left=0.1,
                                       right=0.95,
                                       top=0.80,
                                       bottom=0.05,
                                       wspace=0.2,
                                       hspace=0.4)

        self.plot_basic = self.fig_basic.add_subplot(1, 1, 1)

# Output basic image to a graphic file
            
        #pylab.figure(figsize=(30,30))
        #pylab.imshow(self.basic_image.T)

        pyplot.imshow(self.basic_image)
        
        self.fig_basic.savefig(self.basic_image_output_graphic_file_name,
                                    format="png",                                
                                    dpi=self.resolution) 

        mpl.pyplot.close(self.fig_basic)

        return(0)
    
#------------------------------------------------------------------------------

    def output_basic_image_fits(self):
        if (self.verbose):
           sys.stdout.write("JB1 : output_basic_image_fits ACTIVATED\n")

# Make basic image output FITS file name

        self.basic_image_output_fits_file_name = self.output_file_name.replace(".png", "_basic.fits")
        self.basic_image_output_fits_file_name = os.path.normpath(self.output_directory + "/" + self.basic_image_output_fits_file_name)
        self.basic_image_output_fits_file_name = os.path.abspath(self.basic_image_output_fits_file_name)
        if (self.verbose):
            sys.stdout.write("JB1 : self.basic_image_output_fits_file_name = " + str(self.basic_image_output_fits_file_name) + "\n")
           
# Write basic image FITS file

        try:
            self.basic_image_hdu = fits.PrimaryHDU()
            self.basic_image_hdu.data = self.basic_image
            self.basic_image_hdu.header["DATETIME"] = "{}".format(str(self.timestamp.astimezone().isoformat(sep="T", timespec="seconds")).strip()) 
            self.basic_image_hdu.header["IN_FILE"] = "{}".format(str(self.spec_name_full).strip())
            self.basic_image_hdu.header["FOV_SIZE"] = "{:4.2f}".format(self.fov_size)
            self.basic_image_hdu.header["PIX_SIZE"] = "{:6.3e}".format(self.pixsize)

            #if (self.verbose):
            #    sys.stdout.write("JB1 : self.basic_image_hdu.header = " + str(self.basic_image_hdu.header) + "\n")
                
            self.basic_image_hdu.writeto(self.basic_image_output_fits_file_name, overwrite=True)
                
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to write basic image to FITS file\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)
            
        return(0)

#------------------------------------------------------------------------------

    def make_cleaned_image(self):
        if (self.verbose):
           sys.stdout.write("JB1 : make_cleaned_image ACTIVATED\n")

# To make the image a bit better, the following does a quick Hogbom CLEAN pass.
# Clearly there are much better ways to do this,
# but it seems like none of them are readily pip-installable,
# so here's a quick version using numpy.

        try:
            self.psf = ducc0.wgridder.ms2dirty(
                self.tbl.getcol("UVW")[~self.autocorr_filter],
                self.spec.getcol("CHAN_FREQ")[0],
                numpy.ones_like(self.vis[~self.autocorr_filter]),
                npix_x=self.img_size*2,
                npix_y=self.img_size*2,
                pixsize_x=self.pixsize,
                pixsize_y=self.pixsize,
                epsilon=1.0e-3,
                do_wstacking=True,
            )
            
            self.psf /= self.psf[self.psf.shape[0]//2, self.psf.shape[1]//2]

        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to generate psf\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)
        
# Set beam parameters

        self.beam_size = 1
        try:
            self.beam = scipy.signal.windows.gaussian(self.psf.shape[0],
                                                      std=self.beam_size)[:, None] * scipy.signal.windows.gaussian(self.psf.shape[0],
                                                                                                                   std=self.beam_size)
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Failure to compute beam\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)
        
# Iterate over image

        self.img_dec   = numpy.array(self.basic_image)
        self.out_image = numpy.zeros_like(self.basic_image)
        self.gain      = 0.1
        self.half_size = self.basic_image.shape[0]//2

        if (self.verbose):
            sys.stdout.write("JB1 : self.num_iterations = " + str(self.num_iterations) + "\n")

        try:
            
            for i1 in range(self.num_iterations):
                self.y_max, self.x_max = numpy.unravel_index(numpy.argmax(self.img_dec), self.img_dec.shape)
                self.val               = self.gain * self.img_dec[self.y_max, self.x_max]
                self.d_y, self.d_x     = ((self.y_max-self.basic_image.shape[0]//2),
                                          (self.x_max-self.basic_image.shape[1]//2))
                self.out_image         += self.val*self.beam[self.half_size-self.d_y:-self.half_size-self.d_y,
                                                             self.half_size-self.d_x:-self.half_size-self.d_x]
                self.img_dec           -= self.val*self.psf[self.half_size-self.d_y:-self.half_size-self.d_y,
                                                            self.half_size-self.d_x:-self.half_size-self.d_x]
        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Iteration failure\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)

# Display cleaned image attributes

        self.cleaned_image = (self.out_image+self.img_dec).T # Transpose image

        if (self.verbose):
            sys.stdout.write("JB1 : self.cleaned_image.dtype = " + str(self.cleaned_image.dtype)  + "\n")
            sys.stdout.write("JB1 : self.cleaned_image.shape = " + str(self.cleaned_image.shape)  + "\n")
            sys.stdout.write("JB1 : self.cleaned_image.ndim  = " + str(self.cleaned_image.ndim)   + "\n")
            sys.stdout.write("JB1 : self.cleaned_image.size  = " + str(self.cleaned_image.size)   + "\n")

        return(0)

#------------------------------------------------------------------------------

    def output_cleaned_image_figure(self):
        if (self.verbose):
           sys.stdout.write("JB1 : output_cleaned_image_figure ACTIVATED\n")

# Make cleaned image output graphic file name

        self.cleaned_image_output_graphic_file_name = self.output_file_name.replace(".png", "_cleaned.png")
        self.cleaned_image_output_graphic_file_name = os.path.normpath(self.output_directory + "/" + self.cleaned_image_output_graphic_file_name)
        self.cleaned_image_output_graphic_file_name = os.path.abspath(self.cleaned_image_output_graphic_file_name)
        if (self.verbose):
            sys.stdout.write("JB1 : self.cleaned_image_output_graphic_file_name = " + str(self.cleaned_image_output_graphic_file_name) + "\n")

# Setup figure
           
        self.fig_cleaned = mpl.pyplot.figure(1, figsize=(8.27, 11.69)) # A4 size        
        self.fig_cleaned.suptitle("JB1 - Cleaned Image\n{}".format(str(self.timestamp.astimezone().isoformat(sep="T", timespec="seconds")).strip())) 
        self.fig_cleaned.text(0.05, 0.93, "Output file name = {}".format(str(self.cleaned_image_output_graphic_file_name).strip()))
        self.fig_cleaned.text(0.05, 0.91, "Input file name = {}".format(str(self.spec_name_full).strip()))
        self.fig_cleaned.text(0.05, 0.89, "Graphical file resoloution (dpi) = {:d}".format(self.resolution))
        self.fig_cleaned.text(0.05, 0.87, "FOV size = {:4.2f}".format(self.fov_size))
        self.fig_cleaned.text(0.05, 0.85, "Pixel size = {:6.3e}".format(self.pixsize))
        self.fig_cleaned.text(0.05, 0.83, "Cleaning type = {}".format(str("Hogbom").strip()))
        self.fig_cleaned.text(0.05, 0.81, "Gain = {:4.2f}".format(self.gain))
        self.fig_cleaned.text(0.05, 0.79, "Number of cleaning iterations = {:d}".format(self.num_iterations))
        
        self.fig_cleaned.subplots_adjust(left=0.1,
                                            right=0.95,
                                            top=0.80,
                                            bottom=0.05,
                                            wspace=0.2,
                                            hspace=0.4)

        self.plot_cleaned = self.fig_cleaned.add_subplot(1, 1, 1)

# Output cleaned image to a graphic file

        #pylab.figure(figsize=(30,30))
        #pylab.imshow(self.cleaned_image.T)

        self.cleaned_image = self.cleaned_image.T # Transpose Image
        pyplot.imshow(self.cleaned_image)

        self.fig_cleaned.savefig(self.cleaned_image_output_graphic_file_name,
                                    format="png",                                
                                    dpi=self.resolution) 

        mpl.pyplot.close(self.fig_cleaned)

        return(0)

#------------------------------------------------------------------------------

    def output_cleaned_image_fits(self):
        if (self.verbose):
           sys.stdout.write("JB1 : output_cleaned_image_fits ACTIVATED\n")

# Make cleaned image output FITS file name

        self.cleaned_image_output_fits_file_name = self.output_file_name.replace(".png", "_cleaned.fits")
        self.cleaned_image_output_fits_file_name = os.path.normpath(self.output_directory + "/" + self.cleaned_image_output_fits_file_name)
        self.cleaned_image_output_fits_file_name = os.path.abspath(self.cleaned_image_output_fits_file_name)
        if (self.verbose):
            sys.stdout.write("JB1 : self.cleaned_image_output_fits_file_name = " + str(self.cleaned_image_output_fits_file_name) + "\n")
           
# Write cleaned image FITS file

        try:
            self.cleaned_image_hdu = fits.PrimaryHDU()
            self.cleaned_image_hdu.data = self.cleaned_image
            self.cleaned_image_hdu.header["DATETIME"] = "{}".format(str(self.timestamp.astimezone().isoformat(sep="T", timespec="seconds")).strip()) 
            self.cleaned_image_hdu.header["IN_FILE"]  = "{}".format(str(self.spec_name_full).strip())
            self.cleaned_image_hdu.header["FOV_SIZE"] = "{:4.2f}".format(self.fov_size)
            self.cleaned_image_hdu.header["PIX_SIZE"] = "{:6.3e}".format(self.pixsize)
            self.cleaned_image_hdu.header["CLEAN"]    = "{}".format(str("Hogbom").strip())
            self.cleaned_image_hdu.header["GAIN"]     = "{:4.2f}".format(self.gain)
            self.cleaned_image_hdu.header["NUM_IT"]   = "{:d}".format(self.num_iterations)
            
            #if (self.verbose):
            #    sys.stdout.write("JB1 : self.cleaned_image_hdu.header = " + str(self.cleaned_image_hdu.header) + "\n")
           
            self.cleaned_image_hdu.writeto(self.cleaned_image_output_fits_file_name, overwrite=True)

        except:
            if (self.verbose):
                sys.stderr.write("JB1 : ERROR : Unable to write cleaned image to FITS file\n")
                sys.stderr.write("JB1 : ERROR : Program Terminating\n")
            return(1)

        return(0)

#------------------------------------------------------------------------------

####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        jb1_cmd_line = sys.argv[1:]

    jb1test     = Jb1()
    jb1test_ret = jb1test.jb1(jb1_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
