
# LittleGrapher

## Introducation to *LittleGrapher*

*LittleGrapher* is a lightweight application for plotting figures of mathematical functions and equations. *LittleGrapher* was written in [Python3](https://www.python.org) with [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) framework and [SymPy](http://www.sympy.org/en/index.html) library, and is open-source released on GitHub. *LittleGrapher* is able to plot figures of various mathematical functions and equations, including implicit functions and plane curves. With powerful symbolic mathematics library SymPy, *LittleGrapher* works efficiently and accurately. Also, PyQt5 framework helps *LittleGrapher* create handy user interfaces available for Windows, MacOS and Linux.

## Commitment and Improvement

*LittleGrapher* is an open-source project released on Github community, thus, we encourage developers interested in this project to help us improve *LittleGrapher*. We would appreciate your suggestions and implementation code.
[Contact us](mailto:wangpeihao@gmail.com) to let us know your ideas.

## Install *LittleGrapher*

*LittleGrapher* is an open-source application written in Python3, thus, to run *LittleGrapher*, you have to ensure that you have installed Python3 on your computer first.

[Check here to download and install Python3.](https://www.python.org/downloads/)

After you install Python3, you may need to install the third-party dependencies. Python3 provides ```pip3``` tool to help you install and manage your site-packages. Also see: https://docs.python.org/3/installing/index.html

First you need to install PyQt5 on your computer. Input the following command into your terminal:

```
pip3 install PyQt5
```

Then you need to install SymPy on your computer. Input the following command into your terminal:

```
pip3 install sympy
```

Since SymPy depends on [Matplotlib](https://matplotlib.org) library, you may need to install Matplotlib afterward by the following command:

```
pip3 install matplotlib
```

After installing all the dependencies, you can clone *LittleGrapher* to your local by the following command:

```
git clone git@github.com:peihaowang/LittleGrapher.git
```

Then ```cd``` to the cloned directory on your local, and run *LittleGrapher* like this:

```
python3 main.py
```

You can put an ```&``` at the end to put *LittleGrapher* working on the backend like this:

```
python3 main.py &
```

## Plotting with *LittleGrapher*

After launching *LittleGrapher* successfully, you can plot with *LittleGrapher*. You can add mathematical functions or equations through the button in the right sidebar, and also you are allowed to hide, delete or edit added expressions. *LittleGrapher* will start to plot figures as soon as you submit the new expression.

Note that, the plotting process takes time to do a large amount of computation, you may not get the figures immediately. But the user interface won't stop responding, since *LittleGrapher* handles plotting in other threads.

In addition, *LittleGrapher* allows users to change the line color of figures, which helps users to distinguish different curves of functions or equations.

## Support

[Email to us](mailto:wangpeihao@gmail.com) for bug report and technical support.

## Special Thanks

1. [Python Software Foundation](https://www.python.org).
2. [The Qt Company Ltd.](http://www.qt.io/).
3. [PyQt5](https://riverbankcomputing.com/software/pyqt/intro).
4. [SymPy](http://www.sympy.org/en/index.html).
5. [Matplotlib](https://matplotlib.org).
6. [ShanghaiTech University](http://www.shanghaitech.edu.cn/).
