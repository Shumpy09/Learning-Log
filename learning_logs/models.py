from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """Temat poznawany przez użytkownika"""
    text = models.CharField(max_length=200)                         # rezerwowanie miejsca na niewielką ilość tekstu: imienia, tytułu itp. - 200 znaków
    date_added = models.DateTimeField(auto_now_add=True)            # przypisanie automatycznie bieżącej daty i godziny w chwili tworzenia nowego tematu przez użytkownika
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):                                              # domyślny atrybut podczas wyświetlania informacji; __str__ zwraca ciąg tekstowy przechowywany w atrybucie text 
        """Zwraca reprezentację modelu w postaci ciagu tekstowego"""
        return self.text


class Entry(models.Model):
    """Konkretne informacje o postępie w nauce"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)      # klucz zewnętrzny; tutaj łączy każdy wpis z określonym tematem, kazdemu tematowi został przypisany klucz; 
                                                                    # on_delete=models.CASCADE - po usunięciu danego tematu, wszystkie powiązane rzeczy powinny być usunięte
    text = models.TextField()                                       # tutaj nie narzucamy żadnych ograniczeń co do wartości
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'enteries'                            # zmiana formy podczas odwłoywania się do więcej niż tylko jednego wpisu

    def __str__(self):                                              # wskazuje, które info mają zostać wyświetlone podczas odwoływania się do poszczególnych wpisów
        """Zwraca reprezentację modelu w postaci ciągu tekstowego"""
        if len(self.text) < 50:
            return f"{self.text}"
        else:
            return f"{self.text[:50]}..."                           # ograniczamy go do 50 znaków

