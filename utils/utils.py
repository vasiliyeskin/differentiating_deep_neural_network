import csv
import random
import sys, os, re, shutil, argparse, logging
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import PIL
from PIL import Image
import numpy as np

import subprocess, shlex
from threading import Timer


TIMEOUT = 30

# replace \pmatrix with \begin{pmatrix}\end{pmatrix}
# replace \matrix with \begin{matrix}\end{matrix}
template = r"""
\documentclass[12pt]{article}
\pagestyle{empty}
\usepackage{amsmath}
\newcommand{\mymatrix}[1]{\begin{matrix}#1\end{matrix}}
\newcommand{\mypmatrix}[1]{\begin{pmatrix}#1\end{pmatrix}}
\begin{document}
\begin{displaymath}
%s
\end{displaymath}
\end{document}
"""


def latex2png(line):
    img_path, l, output_path, replace = line
    pre_name = output_path.replace('/', '_').replace('.','_')
    l = l.strip()
    l = l.replace(r'\pmatrix', r'\mypmatrix')
    l = l.replace(r'\matrix', r'\mymatrix')
    # remove leading comments
    l = l.strip('%')
    if len(l) == 0:
        l = '\\hspace{1cm}'
    # \hspace {1 . 5 cm} -> \hspace {1.5cm}
    for space in ["hspace", "vspace"]:
        match = re.finditer(space + " {(.*?)}", l)
        if match:
            new_l = ""
            last = 0
            for m in match:
                new_l = new_l + l[last:m.start(1)] + m.group(1).replace(" ", "")
                last = m.end(1)
            new_l = new_l + l[last:]
            l = new_l
    if replace or (not os.path.exists(output_path)):
        tex_filename = pre_name+'.tex'
        log_filename = pre_name+'.log'
        aux_filename = pre_name+'.aux'
        with open(tex_filename, "w") as outputfile:
            outputfile.write(template%l)
        run("pdflatex -interaction=nonstopmode %s  >/dev/null" % tex_filename, TIMEOUT)
        os.remove(tex_filename)
        os.remove(log_filename)
        os.remove(aux_filename)
        pdf_filename = tex_filename[:-4]+'.pdf'
        png_filename = tex_filename[:-4]+'.png'
        if not os.path.exists(pdf_filename):
            print('cannot compile')
        else:
            os.system("convert -density 200 -quality 100 %s %s"%(pdf_filename, png_filename))
            os.remove(pdf_filename)
            if os.path.exists(png_filename):
                crop_image(png_filename, output_path)
                os.remove(png_filename)



def crop_image(img, output_path, default_size=None):
    old_im = Image.open(img).convert('L')
    img_data = np.asarray(old_im, dtype=np.uint8) # height, width
    nnz_inds = np.where(img_data!=255)
    if len(nnz_inds[0]) == 0:
        if not default_size:
            old_im.save(output_path)
            return False
        else:
            assert len(default_size) == 2, default_size
            x_min,y_min,x_max,y_max = 0,0,default_size[0],default_size[1]
            old_im = old_im.crop((x_min, y_min, x_max+1, y_max+1))
            old_im.save(output_path)
            return False
    y_min = np.min(nnz_inds[0])
    y_max = np.max(nnz_inds[0])
    x_min = np.min(nnz_inds[1])
    x_max = np.max(nnz_inds[1])
    old_im = old_im.crop((x_min, y_min, x_max+1, y_max+1))
    old_im.save(output_path)
    return True

def run(cmd, timeout_sec):
    proc = subprocess.Popen(cmd, shell=True)
    kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        stdout,stderr = proc.communicate()
    finally:
        timer.cancel()