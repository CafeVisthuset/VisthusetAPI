from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
'''
TODO:
* Gör det möjligt att räkna ut lön, skatt och antal arbetade timmar för varje anställd
    - Ge digitalt lönebesked
* Gör formulär för admin att kunna lägga in antalet timmar de anställda jobbat
    - Uppdaterar automatiskt hours_worked

'''
class Employee(models.Model):
    user = models.OneToOneField(
        User,
        limit_choices_to = {'is_staff' : True},
        null = True,
        blank = True,
        verbose_name='anställd'
        )
    person_number = models.IntegerField(null= True, verbose_name= 'Personnummer')
#    phone_number = models.IntegerField()
    
    wage = models.DecimalField(verbose_name= 'Lön',
        max_digits=6, decimal_places=2, blank=True)
    
    hours_worked = models.DecimalField(verbose_name='arbetade timmar',
        max_digits=6, decimal_places=2, default = 0)
    
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=33.0,
                              help_text='Preliminärskatt att dra från lönen',
                              verbose_name='preliminärskatt')
    
    drawTax = models.BooleanField(default=True, verbose_name='Dra preliminärskatt',
                                  help_text='skall preliminärskatt dras från lönen?')
    
    ArbAvg = models.DecimalField(max_digits=3, decimal_places=2, default=0.25)
    
    def get_full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
    
    def update_hours_worked(self):
        pass
    
    class Meta:
        verbose_name = 'anställd'
        verbose_name_plural = 'anställda'
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.employee.save()
    
class Dagskassa(models.Model):
    date = models.DateField(default= date.today, verbose_name='datum')
    
    cash = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='kontanter')
    
    card = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='kort')
    
    cafeSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='café')
    
    iceCreamSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='glass')
    
    foodShopSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='gårdsbutik')
    
    bikeSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='cyklar')
    
    booksSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='böcker')
    
    other12Sales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='övrigt 12%')
    
    other25Sales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='övrigt 25%')
    
    signature = models.ForeignKey(Employee,
        on_delete=models.CASCADE,
        verbose_name='Signatur'
        )
    
    comment = models.CharField(max_length = 150, null=True, verbose_name='kommentar')
    
    class Meta:
        verbose_name = 'dagskassa'
        verbose_name_plural = 'dagskassor'
        ordering = ('date', )
        
