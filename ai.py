import numpy
from PIL import (
    Image,
    ImageEnhance,
    ImageOps,
    UnidentifiedImageError,
)
import pickle

def calc_number(image):

    try:
        # 画像を開く
        im = Image.open(image.file)
    except UnidentifiedImageError:
        return '画像が開けません/画像が添付されているかを確認してください'
    except Exception as e:
        print('予期せぬエラーが発生しました')
        print('* 種類:', type(e))
        print('* 内容:', e)

    try:
        #学習済みモデルのロード
        with open('trained-model.pickle', 'rb') as b:
            clf = pickle.load(b)
    except Exception as e:
        print('学習済みモデルのロードに失敗しました/モデルが存在するかを確認してください')
        print('* 種類:', type(e))
        print('* 内容:', e)

    try:
        #前処理
        im = ImageEnhance.Brightness(im).enhance(2) #明るさを調整（明瞭化）
        im = im.convert(mode='L') #グレースケール（モノクロ）に変更
        im = im.resize((8,8)) #文字を縮小化（8×8のピクセルへリサイズ）
        im = ImageOps.invert(im) #明暗を反転
        X_bin = numpy.asarray(im) #2次元配列に変換
        X_bin = X_bin.reshape(1, 64) #1次元配列に変換
        X_bin = X_bin * (16/255) #0~255から0~16の数値へ変換

        #予測
        y_pred = clf.predict(X_bin) #学習済みのモデルから、画像の数値を予測
        y_pred = y_pred[0] #予測結果を出力
        return y_pred
    
    except Exception as e:
        print('数値判別処理で予期せぬエラーが発生しました')
        print('* 種類:', type(e))
        print('* 内容:', e)

def judge(image=None):
    response = ''
    try:
        result = calc_number(image)
        if isinstance(result, str):
            response = result
        else:
            response = 'この数字は「{}」です'.format(result)

        return response

    except Exception as e:
        print('予期せぬエラーが発生しました')
        print('* 種類:', type(e))
        print('* 内容:', e)