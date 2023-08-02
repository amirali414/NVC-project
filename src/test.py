from sklearn.linear_model import LinearRegression

# داده‌های آموزشی برای تخمین قیمت خودروها
# در اینجا فقط به‌عنوان مثال، دو ویژگی (سن و کیلومتر) را برای تخمین استفاده می‌کنیم
data = [
    [1, 10000],
    [2, 15000],
    [3, 20000],
    [4, 25000],
    [5, 30000]
]

# قیمت‌های متناظر با داده‌های آموزشی (برحسب میلیون تومان)
prices = [10, 15, 20, 25, 30]

# ایجاد مدل رگرسیون خطی
model = LinearRegression()

# آموزش مدل با داده‌های آموزشی
model.fit(data, prices)

# ورودی جدید برای تخمین قیمت خودرو
new_data = [
    [6, 35000],
    [7, 40000]
]

# تخمین قیمت خودرو برای ورودی‌های جدید
predicted_prices = model.predict(new_data)

# چاپ نتایج تخمین
for i, data_point in enumerate(new_data):
    print(f"برای خودرو با سن {data_point[0]} سال و {data_point[1]} کیلومتر، قیمت تخمینی: {predicted_prices[i]} میلیون تومان")
