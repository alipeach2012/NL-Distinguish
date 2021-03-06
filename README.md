# NL-Distinguish

因为不同地区的人群对汉语拼音中N和L的分辨能力是不同的，所以本代码用于自行训练对汉语拼音中N和L的训练。本代码中自带的拼音词库来源 https://github.com/mozillazg/phrase-pinyin-data 。

**一.main-gui.py**

代码中，main-gui.py 是编写的图形界面下的训练程序。

![image](https://github.com/alipeach2012/NL-Distinguish/blob/master/imgs/gui.png)
具体效果可以参见视频 https://github.com/alipeach2012/NL-Distinguish/tree/master/imgs/GUI.mp4 


**二.main-sever.py**

代码中，main-sever.py为基于天猫精灵平台实现的小技能，其中main-sever.py的代码需在服务器运行，在天猫精灵开发者平台配置后，通过webhook实现通讯功能。基本的通讯功能代码参考了
https://bbs.hassbian.com/thread-7011-1-6.html 的帖子。具体实现效果可以参见视频 https://github.com/alipeach2012/NL-Distinguish/tree/master/imgs/天猫精灵.mp4

其中需要在天猫精灵开者者平台配置如下：

1.设置实体
![image](https://github.com/alipeach2012/NL-Distinguish/blob/master/imgs/st1.png)


2.设置意图
![image](https://github.com/alipeach2012/NL-Distinguish/blob/master/imgs/yt4.png)
其中三个意图分别为回答问题，启动对话，结束对话。具体设置分别如下：
![image](https://github.com/alipeach2012/NL-Distinguish/blob/master/imgs/yt1.png)
设置结束游戏的意图
![image](https://github.com/alipeach2012/NL-Distinguish/blob/master/imgs/yt2.png)
设置回答问题的意图
![image](https://github.com/alipeach2012/NL-Distinguish/blob/master/imgs/yt3.png)
设置开始游戏的意图

3.设置回复
![image](https://github.com/alipeach2012/NL-Distinguish/blob/master/imgs/hf.png)
指令通过webhook转发，解析结果后将结果反馈给天猫精灵。所以需要有一台服务器，运行main-sever.py程序，并在天猫精灵中设置转发和验证文件。

**三.学习设置**

每个词组出现概率是动态的，会有本地文件每次记录，答错一次，该词组下次出现概率变为两倍，答对一次，该词组下次出现概率变为上次的二分之一。


这个项目是为了纪念我和我室友的友谊，希望能把你写成code，祝你一切安好。

