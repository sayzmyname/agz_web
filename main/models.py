from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100) # чарфилд - поле для ввода текста (текст,символы и циферки)
    slug = models.CharField(max_length=100, unique=True) # слаг нам нужен чтобы правильно генерировать юрлки (допустим domen.com/product/234234(наш артикул условный) и наша юрлка из набора циферок превращается в читабельную ссылку (тоесть мы добавили слаг, и с ним наша юрлка будет выглядеть вот так: domen.com/product/futbolka-chornaya))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
       return self.name

class Size(models.Model):
    name = models.CharField(max_length=20) #тут мы отвечаем за размер, например S L XL 



    def __str__(self):
        return self.name
    

class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='product_size')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveBigIntegerField(default=0) #количество которое люди могут купить

    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock) for {self.product.name}"
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products') #наследуем
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products/main/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

  
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name
      
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name='images')
    image = models.ImageField(upload_to='products/extra/')


#поскольку у нас магазин одежды, в мейне мы прописываем нашу одежду.
# все это нам нужно для того чтобы выяснить состояния. В нашем сайте мы хотим видеть (category, name, slug, color, price, desc, images)
