from django.contrib import admin
from accounting_double_entry.models import Pl_journal, journal,group1,ledger1,selectdatefield,Payment,Particularspayment,Receipt,Particularsreceipt,Contra,Particularscontra,Multijournal,Multijournaltotal
from accounting_double_entry.forms import Ledgerformadmin
# Register your models here.

class group1admin(admin.ModelAdmin):
	model = group1
	list_display = ['group_Name','urlhash', 'Master','balance_nature']
	search_fields = ['group_Name','urlhash']
	readonly_fields = ('User',)


class journaladmin(admin.ModelAdmin):
	model = journal
	list_display = ['By', 'To','Debit','Credit']
	search_fields = ['By','To']
	readonly_fields = ('User',)


class journaltransactionsdebit(admin.TabularInline):
	model = journal
	fk_name = 'By'
	exclude = ['Credit', 'Total_Debit', 'Total_Credit']
	

class journaltransactionscredit(admin.TabularInline):
	model = journal
	fk_name = 'To'
	exclude = ['Debit', 'Total_Credit', 'Total_Debit']
	
class ledgerAdmin(admin.ModelAdmin):
	model = ledger1
	list_display = ['Creation_Date', 'name','Opening_Balance']
	search_fields = ['name']
	readonly_fields = ('User',)
	inlines = [
           journaltransactionsdebit,
           journaltransactionscredit,
           ]

class paymentinline(admin.TabularInline):
	model = Particularspayment
	fk_name = 'payment'

class PaymentAdmin(admin.ModelAdmin):
	model = Payment
	list_display = ['date', 'account','total_amt']
	search_fields = ['account']
	inlines = [
           paymentinline,
           ]

class receiptinline(admin.TabularInline):
	model = Particularsreceipt
	fk_name = 'receipt'

class ReceiptAdmin(admin.ModelAdmin):
	model = Receipt
	list_display = ['date', 'account','total_amt']
	search_fields = ['account']
	inlines = [
           receiptinline,
           ]

class contrainline(admin.TabularInline):
	model = Particularscontra
	fk_name = 'contra'

class ContraAdmin(admin.ModelAdmin):
	model = Contra
	list_display = ['date', 'account','total_amt']
	search_fields = ['account']
	inlines = [
           contrainline,
           ]

class multijournalinline(admin.TabularInline):
	model = Multijournal
	fk_name = 'total'

class multijournalAdmin(admin.ModelAdmin):
	model = Multijournaltotal
	list_display = ['Date', 'Total_Debit','Total_Credit']
	inlines = [
           multijournalinline,
           ]

admin.site.register(ledger1,ledgerAdmin)
admin.site.register(group1,group1admin)
admin.site.register(journal,journaladmin)
admin.site.register(selectdatefield)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Particularspayment)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Particularsreceipt)
admin.site.register(Contra, ContraAdmin)
admin.site.register(Particularscontra)
admin.site.register(Multijournaltotal, multijournalAdmin)
admin.site.register(Pl_journal)





