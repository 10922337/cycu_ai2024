from sklearn import datasets
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 加載數據集
iris = datasets.load_iris()
X = iris.data
y = iris.target

print(f"原始資料集：\n特徵：\n{X[:5]}\n目標：\n{y[:5]}")

# 切分數據集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"訓練資料：\n{X_train[:5]}\n訓練目標：\n{y_train[:5]}")
print(f"測試資料：\n{X_test[:5]}\n測試目標：\n{y_test[:5]}")

# 特徵標準化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 創建SVM分類器實例，這裡使用預設的核函數（RBF核）
model = SVC(kernel='rbf', decision_function_shape='ovo')

# 訓練模型
model.fit(X_train, y_train)

# 進行預測
y_pred = model.predict(X_test)

print(f"預測結果：\n{y_pred[:5]}")

# 計算準確率
accuracy = accuracy_score(y_test, y_pred)

print(f"預測準確率為: {accuracy:.2f}")

# 進行交叉驗證
scores = cross_val_score(model, X, y, cv=5)

print(f"交叉驗證分數: {scores}")
print(f"交叉驗證分數平均值: {scores.mean():.2f}")