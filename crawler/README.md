### 下载小工具

#### 目前实现下载weiqtv.com的视频
#####使用示例：
1. python3 main.py
2. python3 main.py http proxy.com:port
  
#####注意事项：
1. main里面的两个参数，一个是weiqtv的某个视频合辑的一集的地址，一个是本地的存放目录
2. 访问weiqitv.com和flvcd.com没有问题的不用管proxy
3. 解析视频用了某个网站的抓取视频的结果，曾经使用过该网站提供的下载工具，不太好用，所以写了这个小工具
4. weiqitv.py里面的format可以选三种，normal,super,real。以猫哥讲定式为例，norma大概60M, super大概240M, real大概500M
5. 没有在windows下测试过
