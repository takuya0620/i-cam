# i-cam
interactive_camera

トラックバーによって動画に補正をかける. 

- コントラスト補正:
RGB各要素にシグモイド関数に従うトーンカーブを適用することで実装.
- 色相, 彩度, 明度補正:
RGB色空間からHSV色空間に変換してからそれぞれの要素をガンマ変換し, その後RGB色空間に逆変換することで実装.
- ガウシアンフィルタ:
GaussianBlurを用いて実装した.

NumPy, OpenCVのライブラリを用いた. 
ガンマ変換のgamma=0の値はより小さい値で補完することで, 直感的にトラックバーを操作できるようにした.
また, 軽量化のために, それぞれのトラックバーでデフォルトの値では画像処理を行っていない.

![画像](fig/i-cam.gif "実際の動作")


S字トーンカーブはシグモイド関数で実装できる.
<http://www.hamanoweb.com/blog/?p=3408>

OpenCVにおける色彩空間の変換
https://bi.biopapyrus.jp/ia/opencv/color-space.html

ガウシアンフィルタを用いた平均化
https://www.blog.umentu.work/python-opencv3%E3%81%A7gaussian%E3%82%AA%E3%83%9A%E3%83%AC%E3%83%BC%E3%82%BF%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E5%B9%B3%E6%BB%91%E5%8C%96/

OpenCVによるフーリエ変換
https://algorithm.joho.info/programming/python/opencv-fft-low-pass-filter-py/
