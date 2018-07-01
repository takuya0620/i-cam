# i-cam
interactive camera

- コントラスト補正はRGB各要素にシグモイド関数に従うトーンカーブを適用することで実装.
- 色相, 彩度, 明度はRGB色空間からHSV色空間に変換してからそれぞれの要素をガンマ変換し, その後RGB色空間に逆変換することで実装.
- ローパスフィルタをFFTを用いて実装した.

ガンマ変換の$\gamma=0$の値はより小さい値で補完することで, 直感的にトラックバーを操作できるようにした.

S字トーンカーブはシグモイド関数で実装できる.
<http://www.hamanoweb.com/blog/?p=3408>

OpenCVにおける色彩空間の変換
https://bi.biopapyrus.jp/ia/opencv/color-space.html

OpenCVによるフーリエ変換
https://algorithm.joho.info/programming/python/opencv-fft-low-pass-filter-py/
