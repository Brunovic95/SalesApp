from kivymd.app import MDApp
from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.uix.popup import Popup
from kivy.core.window import Window 
from kivy.uix.scrollview import ScrollView 
from datetime import date,datetime,time
from kivy.uix.relativelayout import RelativeLayout 
import re
import calendar
from kivy.animation import Animation 
from kivy.uix.spinner import Spinner 
from kivy.uix.floatlayout import FloatLayout 
from kivy.clock import Clock
from kivy.uix.image import Image 
from kivy.uix.filechooser import FileChooserIconView 
from kivy.uix.boxlayout import BoxLayout 
import random 
from PIL import Image as PILImage, ExifTags
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager


def send_code():
        my_code=random.randint(100000,999999)
        users=Database(['users.db'])
        user=users.get_user_info("users.db")[0]
        my_send_mail(
        f'Verification code for {user[2]}',
        f'email - {user[3]}\n customer name - {user[2]}\ncode - {my_code}','nambalebruno026@gmail.com',
        logic=lambda:insert_code(my_code))
                
         
def insert_code(code):
    db=Database(['has_access'])
    db.has_access('has_access', code=code)

def correct_image_orientation(path):
        """Check EXIF orientation and rotate the image if needed."""
        try:
            img = PILImage.open(path)

            # Check if EXIF orientation exists
            exif = img._getexif()
            if exif:
                for tag, value in ExifTags.TAGS.items():
                    if value == 'Orientation':
                        orientation_tag = tag
                        break
                else:
                    return path  # No orientation tag, return original path

                if orientation_tag in exif:
                    orientation = exif[orientation_tag]

                    # Rotate the image based on EXIF orientation
                    if orientation == 3:  # Upside down
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:  # Rotated 90° CW
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:  # Rotated 90° CCW
                        img = img.rotate(90, expand=True)

                    # Save the corrected image
                    corrected_path = path.replace(".jpg", "_fixed.jpg").replace(".png", "_fixed.png")
                    img.save(corrected_path)
                    return corrected_path
        except Exception as e:
            print("Error correcting image orientation:", e)

        return path  # Return original if anything goes wrong

def pop_msg(title,msg,function=None):
    
    pop=Popup(title =title,size_hint=(None,None), size=(500,500))
    pop_body=GridLayout(cols=1)
    pop_body.add_widget(Label(text =msg,size_hint_y=0.8,text_size=(480,None),padding_x=50,bold=True, font_size=25))
    btn=GridLayout(cols =2,size_hint_y =0.2)
    btn.add_widget(Button(text ='ok',on_press=lambda instance:(close_pop(instance, pop,function=function))))
    if function:
        
        btn.add_widget(Button(text ='check',on_press=lambda instance:(close_pop(instance, pop,function=function))))
    pop_body.add_widget(btn)
    pop.content =pop_body
    pop.open()
    
def close_pop(instance,pop,function):
    
    if function:
        if instance.text =='check':
            function()
    pop.dismiss()
    
def date_diff(your_date):
    date_format = '%Y-%m-%d'  # Corrected format
    given_date = datetime.strptime(your_date, date_format)  # Parse input string into a datetime object
    today = datetime.today()  # Get today's date
    no_of_days = (today - given_date).days  # Calculate difference in days
    return no_of_days
    
    
def send_email(instance,mail,msg,recipient,logic=None):
    my_send_mail(mail,msg,recipient, logic=logic)
    
def my_send_mail(mail,msg,recipient,logic=None):
        
        
            try:
                sender = 'dnbrunovicmedia@gmail.com'
                receiver = recipient
                password = 'amzxqfatbfjjktej'
                subject =mail
                message = msg
                msg = MIMEText(message)
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = receiver
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
                
                server.quit()
                if logic:
                    logic()
                
            except smtplib.SMTPAuthenticationError:
                pop_msg( 'invalid email address','please check your email address')
            except smtplib.SMTPRecipientsRefused:
                pop_msg( 'invalid email address','please check your email address')
            except smtplib.SMTPException as e:
                pop_msg( 'invalid email address','please check your email address')
            except Exception as e:
                pop_msg('error','error occurred while processing your request or you currently have no Internet connection')
   
def date_input_filter(text):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, text):
        return text
    else:
        return ''
        
def back_btn(parent,function):
    layout =FloatLayout(size_hint =(None,None) , height =100,width=Window.size[0])
    layout.add_widget(Button(text ='<',font_size=60,background_color='white',size_hint=(None, None), size=(100,100),pos_hint={'x':0.85,'top':0.95,},color=(0,0,0,1) ,on_press=lambda instance:function(instance)))
    parent.add_widget(layout)
    
def low_stock():
    lst=[]
    db=Database(['products.db', 'sales_details.db', 'stock_details.db'])
    data=db.product_stock(['products.db', 'sales_details.db', 'stock_details.db'])
    db2=Database(['products.db'])
    for row in data:
        if row:
            total_qty=data[row][1]-data[row][0]
            name=db2.selected_product('products.db', row)
            if total_qty<=name[3]:
                lst.append(row)
    return lst
    
    
class CalendarWidget(BoxLayout):
    def __init__(self,on_date_selected=None, **kwargs):
        super(CalendarWidget, self).__init__(**kwargs)
        self.on_date_selected=on_date_selected
        self.block=RelativeLayout()
        self.add_widget(self.block)
        self.block.add_widget(TextInput(readonly =True, background_color =(0,0,1,0.4 ),disabled=True))
        self.grid=GridLayout(cols =1)
        self.block.add_widget(self.grid)
        self.selected_date=None
        self.orientation = 'vertical'
        self.year = int(datetime.now().year)
        self.month = int(datetime.now().month)
        
        self.display_calendar()

    def display_calendar(self):
        year_disp=TextInput(text =str(datetime.now().year),font_size=25)
        mon_disp=TextInput(text =str(datetime.now().strftime('%B')),font_size=25)
        year_values =[str(i) for i in range(int(datetime.now().year),2009,-1)]
        mon_dict = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
        mon_values=[]
        year_grid=RelativeLayout()
        year_grid.add_widget(year_disp)
        year_grid.add_widget(Label(text ='v',size_hint_x=None, width=50,pos_hint={'x':0.8}, color=(0,0,0,1), font_size=50))
        mon_grid=RelativeLayout()
        mon_grid.add_widget(mon_disp)
        mon_grid.add_widget(Label(text ='v',size_hint_x=None, width=50,pos_hint={'x':0.8}, color=(0,0,0,1), font_size=50))
        box=BoxLayout(orientation='horizontal',size_hint_y=0.15)
        self.year_spinner =Spinner(opacity=0,values=year_values)
        self.month_spinner =Spinner(opacity=0)
        self.month_spinner.bind(text = lambda instance, value :self.on_text_change(instance, value, mon_disp,mon_dict,mon_values, mon=self.month))
        self.year_spinner.bind(text = lambda instance, value :self.on_text_change(instance, value, year_disp,mon_dict,mon_values, yr=self.year))
        if year_disp.text == str(datetime.today().year):
            mon_values.clear()
            for i in range(1, datetime.now().month + 1):
                mon_values.append(mon_dict[i])
        else:
            mon_values.clear()
            mon_values = list(mon_dict.values())
        self.month_spinner.values=mon_values          
        year_grid.add_widget(self.year_spinner)
        mon_grid.add_widget(self.month_spinner)
        box.add_widget(year_grid)
        box.add_widget(mon_grid)
        data=['mon','tue','wed','thu','fri','sat','sun']
        grid=GridLayout(cols =7,size_hint_y =0.15)
        self.grid.add_widget(box)
        self.grid.add_widget(grid)
        
        for dat in data:
            grid.add_widget(Label(text =dat,bold=True, font_size=25))
        
        self.layout=GridLayout(cols =1,size_hint_y=0.7)
        
        self.grid.add_widget(self.layout)
        self.my_calendar()
        
        
        
    def my_calendar(self):
        self.layout.clear_widgets()
        cal = calendar.monthcalendar(self.year, self.month)
        for week in cal:
            row = BoxLayout()
            
            for day in week:
                if day == 0:
                    row.add_widget(Label(text=''))
                else:
                    btn=Button(text=str(day),on_press=self.my_date)
                    if self.year==int(datetime.now().year) and self.month==int(datetime.now().month):
                        if day>int(datetime.now().day):
                            btn.disabled =True
                    row.add_widget(btn)
            self.layout.add_widget(row)
        
        
    def my_date(self,instance):
       
        self.selected_date =f'{self.year}-{self.month:02}-{instance.text}'
        if self.on_date_selected:
            self.on_date_selected(self.selected_date)
        
    def on_text_change(self, instance, value, ctrl, dict, my_list, mon=None, yr=None):
        if value:
            if mon:
                ctrl.text = value
                for k, v in dict.items():
                    if value == v:
                        self.month = int(k)
            if yr:
                ctrl.text = value
                self.year = int(value)
                my_list.clear()
                if value == str(datetime.today().year):
                    for i in range(1, datetime.now().month + 1):
                        my_list.append(dict[i])
                else:
                    my_list.extend(dict.values())
                self.month_spinner.values = my_list  # Update the spinner values!
            self.my_calendar()

class FreeTrial(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
        super(FreeTrial,self).__init__(**kwargs)
        self.cols =1
        self.logged_in_user =logged_in_user 
        self.add_widget(Label(bold=True,font_size =30,text_size =(Window.size[0],None),text='You are having two(2) weeks free trial\nPlease you will be required to subscribe in order to access our services. \nThanks for using our service!.', color=(0,0,0,1), padding=(20,20,20,20)))
        Clock.schedule_once(self.home_page,10)
        
    def home_page(self,dt):
         self.clear_widgets()
         self.add_widget(MainMenu(self.logged_in_user))
         
class ShowImagePicker(BoxLayout):
    def __init__(self,logged_in_user,**kwargs):
        self.logged_in_user =logged_in_user
        super().__init__(orientation="vertical", **kwargs)

        # Create the button and image widget
        self.pick_button = MDRaisedButton(text="Pick Image", size_hint_y=0.1)
        self.pick_button.bind(on_release=self.file_manager_open)

        self.image_view = Image(size_hint_y=0.8, allow_stretch=True, keep_ratio=True,source='')

        # Add widgets to layout
        self.add_widget(self.pick_button)
        self.add_widget(self.image_view)
        grid=GridLayout(cols =2,size_hint_y=0.1)
        grid.add_widget(Button(text ='cancel',on_press=self.admin_page))
        grid.add_widget(Button(text='select this image',on_press=self.select_image))
        self.add_widget(grid)

        # Initialize file manager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path, ext=['.jpg','.png']
        )
    def admin_page(self,instance):
        self.clear_widgets()
        self.add_widget(AdminPage(self.logged_in_user)) 
        
    def file_manager_open(self, *args):
        self.file_manager.show("/storage/emulated/0/")  # Opens internal storage

    def select_path(self, path):
        corrected_path =correct_image_orientation(path)
        self.image_view.source = corrected_path  # Update the image source
        self.image_view.reload()  # Force UI refresh
        self.exit_manager()


    def exit_manager(self, *args):
        self.file_manager.close()
        
    def select_image(self, instance):
        if self.image_view.source!='':
            db=Database(['company_logo'])
            img=db.get_company_logo('company_logo')
            if not img:
                db.add_company_logo('company_logo',self.image_view.source)
            else:
                db.update_company_logo('company_logo',self.image_view.source) 
            self.clear_widgets()
            self.add_widget(MainMenu(self.logged_in_user))
                
class Help(GridLayout):
    def __init__(self, logged_in_user,**kwargs):
        super(Help, self).__init__(**kwargs)
        self.cols = 1
        self.logged_in_user =logged_in_user 
        
        # Main layout container
        self.block_layout = RelativeLayout()
        
        # Scrollable content block
        self.block = GridLayout(cols=1, size_hint_y=None)
        self.block.bind(minimum_height=self.block.setter('height'))  # Ensure dynamic height adjustment
        
        # Add a disabled TextInput at the top
        self.block_layout.add_widget(TextInput(disabled=True, size_hint_y=1))
        
        # Container for buttons
        block = GridLayout(cols=1)
        btn = GridLayout(cols=2, size_hint_y=0.1)
        block.add_widget(btn)

        # Back button
        btn.add_widget(MDRaisedButton(text='<< Back', size_hint_x=0.3, on_release=self.main_menu, font_size=30))
        btn.add_widget(Label(text='', size_hint_x=0.7))  # Spacer

        # ScrollView
        scroll = ScrollView(size_hint_y=0.85)  # Adjusted to take most of the screen
        self.block_layout.add_widget(block)
        block.add_widget(scroll)
        scroll.add_widget(self.block)

        self.add_widget(self.block_layout)
        self.blank=Label(text ='',size_hint_y=0.05)
        block.add_widget(self.blank)
        # Help text
        lbl = Label(
            font_size=25, size_hint_y=None, color=(0, 0, 0, 1),
            text_size=(Window.size[0] * 0.9, None), padding=[20, 50, 20, 50], markup=True
        )
        lbl.text = '''[b]Thank you for visiting Dñ Břûñõvîç Data Inventory System's help page.[/b]
             Please let me explain how every control on the main menu works. 
      [b]1. Sales page[/b]: 
              This page is the main page where all sales take place. Please make sure to press the new sale button for every new sale to avoid adding products to your last sale. In case of any mistake, please check the box on the left-hand side of the product you made to enable editing or deletion. You can check all the day's sales, where the summary of all products sold is arranged, by pressing on today's sales. 
      [b]2. Products:[/b] 
              Here, you will go straight to the add new product window, where you are supposed to enter only new products. You can also check all the products in the table by pressing on the products table. You can edit product names or prices directly from the product table. Note that any changes made cannot be undone and will affect the whole data on this application, i.e., if you change the price, this price will be reflected everywhere the price is reflected.
       [b]3. Today's Report:[/b] 
               This is the most important area where you can see your day's performance. It shows the summary of all sales, purchases, expenses, and other incomes entered into the business, which are not part of the business. Here, you will know how much you have spent, sold, gained, and how much you have at hand. 
               
       If you have any inquiries or suggestions;
       
       You can us well reach us on +256 778659178 or +256 703567584
       
        or send your query in our mail box below:
        Thanks for you support!'''

        # Adjust height dynamically
        lbl.bind(texture_size=lambda instance, texture_size: setattr(instance, 'height', texture_size[1]))

        # Email form section
        mail_block = GridLayout(cols=1, size_hint_y=None)
        mail_block.bind(minimum_height=mail_block.setter('height'))  # Ensure dynamic height

        mail_block.add_widget(Label(text='Send us A message', bold=True, color=(0, 0, 0, 1), font_size=40, size_hint_y=None, height=100))

        mail_entry = TextInput(hint_text='Enter your email address or phone number', size_hint_y=None, height=100)
        mail_entry.bind(focus=lambda instance, value: self.on_focus(instance, value, scroll))
        mail_block.add_widget(mail_entry)

        mail = TextInput(hint_text='Write a message', size_hint_y=None, height=200)
        mail.bind(focus=lambda instance, value: self.on_focus(instance, value, scroll))
        mail_block.add_widget(mail)

        send_button = Button(text='Send', size_hint_y=None, height=100)
        send_button.bind(on_press=lambda instance: send_email(instance,'A message from '+mail_entry.text,f'{mail_entry.text} \n {mail.text}','nambalebruno026@gmail.com',logic=lambda :self.clear_mail(mail,mail_entry)))
        mail_block.add_widget(send_button)

        # Add all components to the scrollable block
        self.block.add_widget(lbl)
        self.block.add_widget(mail_block)
        
        
    def clear_mail(self,mail,mail_entry):
        mail_entry.text=''
        mail.text=''
        
              
    def main_menu(self, instance):
        self.clear_widgets()
        self.add_widget(MainMenu(self.logged_in_user))
        
    
           
           
    def on_focus(self,instance,value,scroll):
        if value:
            scroll.size_hint_y=0.4
            self.blank.size_hint_y=0.5
            scroll.scroll_y=0
        else:
            scroll.size_hint_y=0.85
            self.blank.size_hint_y=0.05
            
            scroll.scroll_y =0
        
class Welcome(GridLayout):
    def __init__(self, **kwargs):
        super(Welcome,self).__init__(**kwargs)
        self.cols=1
        self.add_widget(Image(allow_stretch =True, keep_ratio =True, source='logo.jpg'))
        Clock.schedule_once(lambda dt :self.my_logic(dt),10)
        
    def my_logic(self,dt):
        db=Database(['users.db'])
        users=db.get_user_info('users.db')
        if len(users)!=0:
            self.clear_widgets()
            self.add_widget(LogIn())
        else:
            self.clear_widgets()
            self.add_widget(SignUp())
        
        
class CheckSubscription(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
        super(CheckSubscription,self).__init__(**kwargs)
        self.cols=1 
        self.logged_in_user =logged_in_user   
        db=Database(['has_access'])
        data=db.has_access('has_access',code=None)
        if data:
            if data[0][1]==0:
                self.clear_widgets()
                self.add_widget(MainMenu(self.logged_in_user))
            else:
                if date_diff(data[0][2])<=14:
                    self.clear_widgets()
                    self.add_widget(FreeTrial(self.logged_in_user))
                else:
                    self.clear_widgets()
                    self.add_widget(HasAccess(self.logged_in_user))
        else:
            self.clear_widgets()
            self.add_widget(FreeTrial(self.logged_in_user))
           
        
class MainMenu(GridLayout):
    def __init__(self, logged_in_user,**kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.cols = 1
        self.logged_in_user =logged_in_user 
        self.block_layout=RelativeLayout()
        self.block =GridLayout (cols =1)
        self.block_layout.add_widget(TextInput(disabled =True, background_color =(1,0.8,1,0.5)))
        stk=low_stock()
        if len(stk)!=0:
            pop_msg('Low Quantity',f'You have {len(stk)} products that have reached or crossed the minimum stock quantity. You can make new order!', function=self.stock_chk)
        scroll=ScrollView()
        self.block_layout.add_widget(scroll)
        scroll.add_widget(self.block)
        img_db=Database(['company_logo'])
        comp_logo=img_db.get_company_logo('company_logo')
        self.add_widget(self.block_layout)
        self.time_label = Label(font_size=50,size_hint_y=0.07,bold=True, color=(0,0,0,1))
        logo=FloatLayout(size_hint=(1,0.15))
        self.image =Image(size_hint=(None,1), width=200,pos_hint={'x':0,'top':1},keep_ratio=False, allow_stretch=True)
        if not comp_logo:
            corrected_path = correct_image_orientation('logo.jpg')
            self.image.source = corrected_path
            
        else:
            corrected_path = correct_image_orientation(comp_logo[1])
            self.image.source = corrected_path
        logo.add_widget(self.image)
        self.block.add_widget(logo)
        Clock.schedule_interval(self.update_time, 1)

        title_label = RelativeLayout(size_hint_y=0.07)
        title_label.add_widget(Button(text='', background_color=(0, 0, 1, 1), size_hint=(1, 1)))
        lbl=Label(font_size=43, color=(1, 1, 1, 1),bold=True)
        name_db=Database(['company_name.db'])
        nam=name_db.get_company_name('company_name.db')
        if nam:
            lbl.text=nam[1]
        else:
            lbl.text='Dñ Bŕûñõvîç Data Inventory System'
        title_label.add_widget(lbl)
        self.block.add_widget(title_label)
        self.block.add_widget(self.time_label)
        users=Database(['users.db'])
        user=users.get_user_details('users.db',self.logged_in_user)
        self.name = user[2]
        self.my_greeting = self.greetings()
        self.greeting_label=Label(text=f'       {self.my_greeting} {self.name}!', size_hint_y=0.07,bold=True, font_size=34,color=(0,0,0,1))
        self.block.add_widget(self.greeting_label)
        Clock.schedule_interval(self.moving_text,0.2)
        Clock.schedule_interval(self.moving_image,0.2)
        dashboard=GridLayout(cols =2,size_hint_y=0.65)
        dashboard.add_widget(Button(text ='sales',background_color='green',font_size=40,on_press=self.sales))
        dashboard.add_widget(Button(text ='purchases',font_size=40,background_color='yellow',on_press=self.stock))
        dashboard.add_widget(Button(text ='products',font_size=40,background_color='pink',on_press=self.products))
        dashboard.add_widget(Button(text ='Other income',font_size=40,background_color='yellow',on_press=self.income))
        dashboard.add_widget(Button(text ='Expenses',font_size=40,background_color='red',on_press=self.exp))
        dashboard.add_widget(Button(text ='admin page', on_press=self.admin_page,font_size=40,background_color='orange'))
        
        dashboard.add_widget(Button(text ='Logout',background_color='purple',font_size=40,on_press=self.logout))
        dashboard.add_widget(Button(text= 'stock management',on_press=self.stock_bal,font_size=40))
        dashboard.add_widget(Button(text='Today Report', on_press=self.sales_report,background_color='blue',bold=True, font_size=40))
        dashboard.add_widget(Button(text='Help', on_press=self.help,background_color='orange',bold=True, font_size=40))
        self.block.add_widget(dashboard)
        
    def help(self,instance):
        self.clear_widgets()
        self.add_widget(Help(self.logged_in_user))
        
    def stock_chk(self):
        self.clear_widgets()
        self.add_widget(StockBalance(self.logged_in_user, low_stock =True))
        
    def sales_report(self,instance):
        self.clear_widgets()
        self.add_widget(SalesReport(self.logged_in_user))
        
    def update_time(self, dt):
        current_time = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
        self.time_label.text = current_time
        
    def stock_bal(self,instance):
        self.clear_widgets()
        self.add_widget(StockBalance(self.logged_in_user))


    def greetings(self):
        current_time = datetime.now().time()
        if current_time < time(12, 0, 0):
            return 'Good morning'
        elif current_time < time(17, 0, 0):
            return 'Good Afternoon'
        else:
            return 'Good Evening'
            
    def moving_image(self, dt):
        x = self.image.pos_hint['x']  
        x += 0.1 
        if x > 0.9:  
            x = 0.1
        self.image.pos_hint = {'x': x}  
        
        
    def moving_text(self,dt,):
        if len(self.greeting_label.text)!=0:
            self.greeting_label.text=self.greeting_label.text[1:]
        else:
            self.greeting_label.text =f'       {self.my_greeting} {self.name}!'
            
        
    def logout(self,instance ):
        self.clear_widgets()
        log=LogIn()
        self.add_widget(log)
        
    def sales(self, instance):
        self.clear_widgets()
        self.add_widget(SalesPage(self.logged_in_user))
        
    def products(self, instance):
        self.clear_widgets()
        self.add_widget(ProductsPage(self.logged_in_user)) 
    
    def income(self, instance):
        self.clear_widgets()
        self.add_widget(IncomeAndExpenses(self.logged_in_user,income=True))
        
    def exp(self, instance):
        self.clear_widgets()
        self.add_widget(IncomeAndExpenses(self.logged_in_user, exp=True)) 
        
    def stock(self, instance):
        self.clear_widgets()
        self.add_widget(Stock(self.logged_in_user))
        

    def admin_page(self, instance ):
        admin=AdminPage(self.logged_in_user)
        self.clear_widgets()
        self.add_widget(admin)
        
        
        
class AdminPage(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
        
        super(AdminPage, self).__init__(**kwargs)
        self.cols =1
        self.logged_in_user =logged_in_user
        self.layout =RelativeLayout()
        grid=GridLayout(cols=2,size_hint_y=0.8)
        layout=GridLayout(cols =1)
        layout.add_widget(Label (text ='Welocome to Admin Page!',size_hint_y=0.1,color=(0,0,0,1), bold=True, font_size=30))
        layout.add_widget (grid)
        self.layout.add_widget(layout)
        self.add_widget(self.layout)
        grid.add_widget(Button(text ='Main Menu',on_press=self.main_menu,background_color='green',bold=True, font_size=30))
        grid.add_widget(Button(text ='User Info',on_press=self.user_info,background_color='pink',bold=True, font_size=30))
        grid.add_widget(Button(text ='Change moving image',background_color='yellow', on_press=self.image_picker,bold=True, font_size=30))
        grid.add_widget(Button(text ='change company name',on_press=self.name_widget,background_color='green',bold=True, font_size=30))
        grid.add_widget(Button(text ='Contact us',on_press=self.help,background_color='pink',bold=True, font_size=30))
        grid.add_widget(Button(text ='upgrade',background_color='yellow', on_press=self.has_access,bold=True, font_size=30))
        
        back_btn(layout,self.main_menu)
       
    def image_picker(self,instance):
        self.clear_widgets()
        self.add_widget(ShowImagePicker(self.logged_in_user))
        
    def main_menu(self,instance):
        self.clear_widgets()
        self.add_widget(MainMenu(self.logged_in_user))
        
    def user_info(self, instance):
         self.clear_widgets()
         self.add_widget(UsersInfo(self.logged_in_user))
         
    def help(self, instance):
         self.clear_widgets()
         self.add_widget(Help(self.logged_in_user))
     
    def has_access(self, instance):
         self.clear_widgets()
         self.add_widget(HasAccess(self.logged_in_user))
         
    def close_panel(self, instance,grid):
         self.layout.remove_widget(grid)
         
    def add_company_name(self,instance,grid):
         if self.name_entry.text!='':
             db=Database(['company_name.db'])
             name=db.get_company_name('company_name.db')
             if name:
                 db.update_company_name('company_name.db',self.name_entry.text)
                 self.layout.remove_widget(grid)
             else:
                 db.add_company_name('company_name.db',self.name_entry.text)
                 self.layout.remove_widget(grid)
             
    def name_widget(self, instance):
        grid=RelativeLayout(size_hint_y =None, height =200,size_hint_x=None, width=500,pos_hint={'y':0.4,'x':0.2})
        grid.add_widget(TextInput(readonly=True, background_color=(0,0,0,1)))
        layout=GridLayout(cols =2)
        layout.add_widget(Label(text ='Company name',size_hint_x=0.4, bold=True))
        self.name_entry =TextInput(hint_text ='enter your company name',size_hint_x=0.6)
        layout.add_widget(self.name_entry)
        layout.add_widget(Button(text ='close', size_hint_x=0.4,on_press=lambda instance :self.close_panel(instance, grid)))
        layout.add_widget(Button(text ='Submit',size_hint_x=0.6,on_press=lambda instance :self.add_company_name(instance, grid)))
        grid.add_widget(layout)
        self.layout.add_widget(grid)
        
                
class UsersInfo(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
        super(UsersInfo,self).__init__(**kwargs)
        self.cols =1
        self.logged_in_user =logged_in_user 
        top=GridLayout(cols =2,size_hint_y =0.07)
        top.add_widget(Button(text ='Back',on_press=self.admin_page))
        top.add_widget(Button(text='User self Registration', on_press=self.signup))
        self.add_widget(top)
        self.add_widget(Label(text ='Only Users with Security Level 1 are able to access this page',color=(0,0,0,1), bold=True,size_hint_y=0.07))
        self.users_block=GridLayout(cols =1,size_hint_y=None)
        self.users_block.bind(minimum_height =self.users_block.setter('height'))
        self.scroll=ScrollView(size_hint_y =0.8)
        self.users_rows =[]
        header=GridLayout(cols =6,size_hint_y=0.06)
        header.add_widget(Button (text ='Id',size_hint_x=0.07,bold=True,font_size=20,background_color='green'))
        header.add_widget(Button (text ='Username',size_hint_x=0.15,bold=True, font_size=20, background_color='green'))
        header.add_widget(Button (text ='Full Name',size_hint_x=0.25,bold=True,font_size=20, background_color='green'))
        header.add_widget(Button (text ='Email',size_hint_x=0.25,bold=True,font_size=20,background_color='green'))
        header.add_widget(Button(text ='security\nLevel',size_hint_x=0.13,bold=True,font_size=20,background_color='green'))
        header.add_widget(Button (text ='password',size_hint_x=0.15,bold=True,font_size=20, background_color='green'))
        self.add_widget(header)
        self.add_widget(self.scroll)
        self.scroll.add_widget(self.users_block)
        self.user_details()
        self.new_user_entry()
        grid=GridLayout(cols =1,size_hint_y =0.07)
        self.add_widget(grid)
        self.keyb=Label(text ='',size_hint_y=0)
        self.add_widget(self.keyb)
                 
    def signup(self, instance):
         self.clear_widgets()
         self.add_widget(SignUp())
         
    def open_keyboard(self, instance, value):
        
        if value:
            self.scroll.size_hint_y = 0.4
            self.keyb.size_hint_y=0.4
            instance_y = instance.y
            content_height =self.users_block.height +100
            ratio = (instance_y ) / content_height 
            self.scroll.scroll_y = ratio
            self.scroll.scroll_to(instance)
        else:
            self.scroll.size_hint_y = 0.8
            self.keyb.size_hint_y =0 
                
        
    def latest_record(self ):
        db=Database(['users.db'])
        user=db.get_last_user_info('users.db')
        layout=GridLayout(cols =6,size_hint_y=None,height=70)
        if user:
            user_id=TextInput(text =str(user[0]),disabled=True,size_hint_x=0.07)
            username =TextInput(text =user[1],size_hint_x=0.15)
            full_names =TextInput(text=user[2],size_hint_x=0.25)
            email=TextInput(text =(str(user[3])),size_hint_x=0.25)
            security_level=TextInput(text =(str(user[4])),size_hint_x=0.13,input_filter='int')
            password =TextInput(text =str(user[5]),size_hint_x=0.15, password=True)
            self.users_rows.append((user_id, username, full_names,email, security_level, password ))
            layout.add_widget(user_id )
            layout.add_widget(username)
            layout.add_widget(full_names )
            layout.add_widget(email)
            layout.add_widget(security_level )
            layout.add_widget(password )
            username.bind(text =self.on_text_change )
            email.bind(text =self.on_text_change )
            full_names.bind(text =self.on_text_change )
            security_level.bind(text =self.on_text_change )
            password.bind(text =self.on_text_change )
            
            self.users_block.remove_widget(self.new_user_widget )
            self.users_block.add_widget(layout)
            self.users_block.add_widget(self.new_user_widget)
        
        
        
    def user_details(self):
        db=Database(['users.db'])
        users=db.get_user_info('users.db')
        layout=GridLayout(cols =6,size_hint_y=None)
        layout.bind(minimum_height =layout.setter('height'))
        layout.clear_widgets()
        
        for user in users:
          user_id=TextInput(text =str(user[0]),disabled=True,size_hint_x=0.07,size_hint_y=None, height=70)
          username =TextInput(text =user[1],size_hint_x=0.15,size_hint_y=None, height=70)
          full_names =TextInput(text=user[2],size_hint_x=0.25,size_hint_y=None, height=70)
          email=TextInput(text=str(user[3]),size_hint_x=0.25,size_hint_y=None, height=70)
          security_level=TextInput(text =(str(user[4])),size_hint_x=0.13,size_hint_y=None, height=70,input_filter='int')
          password =TextInput(text =str(user[5]),size_hint_x=0.15,size_hint_y=None, height=70, password=True)
          self.users_rows.append((user_id, username, full_names, email,security_level, password ))
          layout.add_widget(user_id )
          layout.add_widget(username)
          layout.add_widget(full_names )
          layout.add_widget(email )
          layout.add_widget(security_level )
          layout.add_widget(password )
          username.bind(focus=self.open_keyboard )
          full_names.bind(focus=self.open_keyboard)
          username.bind(text =self.on_text_change )
          security_level.bind(focus=self.open_keyboard)
          email.bind(focus=self.open_keyboard)
          password.bind(focus=self.open_keyboard)
          full_names.bind(text =self.on_text_change )
          security_level.bind(text =self.on_text_change )
          email.bind(text =self.on_text_change )
          password.bind(text =self.on_text_change )
        self.users_block.add_widget(layout)
        self.new_user_widget=GridLayout(cols =6,size_hint_y =None, height =70)
        self.new_user_widget.clear_widgets()
        self.users_block.add_widget(self.new_user_widget)
        
    def admin_page(self, instance):
        self.clear_widgets()
        self.add_widget(AdminPage(self.logged_in_user))
        
    def new_user_entry(self):
        self.new_id=TextInput(size_hint_x =0.07, size_hint_y =None, height =70,disabled=True,text='New')
        self.new_username=TextInput(size_hint_x =0.15 )
        self.new_fullnames=TextInput(size_hint_x =0.25)
        self.new_email=TextInput(size_hint_x=0.25)
        self.new_security=TextInput(size_hint_x =0.13,input_filter ='int')
        self.new_password=TextInput(size_hint_x =0.15, password=True)
        
        self.new_user_widget.add_widget(self.new_id)
        self.new_user_widget.add_widget(self.new_username)
        self.new_user_widget.add_widget(self.new_fullnames)
        self.new_user_widget.add_widget(self.new_email)
        self.new_user_widget.add_widget(self.new_security)
        self.new_user_widget.add_widget(self.new_password)
        self.new_username.bind(focus =self.open_keyboard)
        self.new_fullnames.bind(focus=self.open_keyboard)
        self.new_security.bind(focus =self.open_keyboard)
        self.new_password.bind(focus=self.open_keyboard)
        self.new_username.bind(text=lambda instance,value :self.on_new_user(instance, value))
        self.new_fullnames.bind(text=lambda instance ,value:self.on_new_user(instance, value))
        self.new_security.bind(text=lambda instance ,value:self.on_new_user(instance, value))
        self.new_password.bind(text=lambda instance,value :self.on_new_user(instance, value))
        self.new_email.bind(text=lambda instance,value :self.on_new_user(instance, value))
        
    def new_fields(self):
        self.users_block.remove_widget(self.new_user_widget)
        self.new_field_layout=GridLayout(cols =6,size_hint_y=None, height=70)
        self.field1=TextInput(size_hint_x =0.07,disabled=True)
        self.field2=TextInput(size_hint_x =0.15)
        self.field3=TextInput(size_hint_x =0.25)
        self.field4=TextInput(size_hint_x =0.25)
        self.field5=TextInput(size_hint_x =0.13,input_filter='int')
        self.field6=TextInput(size_hint_x =0.15,password=True)
        self.new_field_layout.add_widget(self.field1)
        self.new_field_layout.add_widget(self.field2)
        self.new_field_layout.add_widget(self.field3)
        self.new_field_layout.add_widget(self.field4)
        self.new_field_layout.add_widget(self.field5)
        self.new_field_layout.add_widget(self.field6)
        self.users_block.add_widget(self.new_field_layout)
        self.field2.bind(focus =lambda instance,value :(self.save_new_users(instance,value), self.open_keyboard(instance, value)))
        self.field3.bind(focus =lambda instance,value :(self.save_new_users(instance,value), self.open_keyboard(instance, value)))
        self.field4.bind(focus =lambda instance,value :(self.save_new_users(instance,value), self.open_keyboard(instance, value)))
        self.field5.bind(focus =lambda instance,value :(self.save_new_users(instance,value), self.open_keyboard(instance, value)))
        self.field6.bind(focus =lambda instance,value :(self.save_new_users(instance,value), self.open_keyboard(instance, value)))
        
    def on_new_user(self,instance,value):
        if value:
            db=Database(['users.db'])
            user=db.get_last_user_id('users.db')
            if user:
                user_id=str(int(user[0])+1)
            else:
                user_id ='1'
            self.new_fields()
        
            if instance ==self.new_username:
                self.field1.text=user_id
                self.field2.text=self.new_username.text
                self.field2.focus=True 
            if instance ==self.new_fullnames:
                self.field1.text=user_id
                self.field3.text=self.new_fullnames.text
                self.field3.focus=True
            if instance ==self.new_email:
                self.field1.text=user_id
                self.field4.text=self.new_email.text
                self.field4.focus=True
            if instance ==self.new_security:
                self.field1.text=user_id
                self.field5.text=self.new_security.text
                self.field5.focus=True
            if instance ==self.new_password:
                self.field1.text=user_id
                self.field6.text=self.password.text
                self.field6.focus=True
                
            self.new_username.text =''
            self.new_fullnames.text=''
            self.new_security.text=''
            self.new_password.text='' 
            self.new_email.text=''
            self.users_block.add_widget(self.new_user_widget)
            
            
    def on_text_change (self,instance, value):
        if value:
            db=Database(['users.db'])
            
            for field in self.users_rows:
              if instance in field:
                  id=field[0].text
                  if instance==field[1]:
                      db.update_user_info('users.db',id,username=field[1].text)
                  elif instance==field[2]:
                      db.update_user_info('users.db',id,full_names=field[2].text)
                  elif instance==field[3]:
                      db.update_user_info('users.db',id,email =field[3].text)
                  elif instance==field[4]:
                      db.update_user_info('users.db',id,security_level =field[4].text)
                  elif instance==field[5]:
                      db.update_user_info('users.db',id,password =field[5].text)
                      
    def save_new_users(self,instance, value):
        layout = instance.parent
        if not any(widget.focus for widget in layout.children if isinstance(widget, TextInput)):
            db=Database(['users.db'])
            db.add_users('users.db', self.field2.text, self.field3.text ,self.field4.text,self.field6.text,security=self.field5.text)
            self.users_block.remove_widget(self.new_field_layout)
            self.field1.text =''
            self.field2.text=''
            self.field3.text=''
            self.field4.text=''
            self.field5.text=''
            self.field6.text=''
            self.latest_record()
              


class HasAccess(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
       
        super(HasAccess,self).__init__(**kwargs)
        self.cols=1
        self.logged_in_user=logged_in_user
        self.db=Database(['has_access'])
        data=self.db.has_access('has_access',code=None)
        
        if data:
            if data[0][1]==0:
                self.paid()
            else:
                self.not_paid(data)
        else:
            send_code()
            self.not_paid(data)
                    
    def not_paid(self,data):
        self.clear_widgets()        
        lbl=Label(text ='You are required to pay for a one time subscription fee of 50,000.ugx on +256 778-659-178 in the names of Nambale Bruno.\nPlease first call the app owner before making any transaction for clarification and for a one time unlock code.\nWe appreciate for your support',bold=True, size_hint_y=None,font_size=30,text_size=(Window.size[0] * 0.9, None) ,color=(0,0,0,1),padding=(20,20,20,20))
        self.add_widget(lbl)
        lbl.bind(texture_size=lambda instance, texture_size: setattr(instance, 'height', texture_size[1]))
        self.add_widget(Label(text ='enter code',size_hint_y=0.1, bold=True, font_size=30, color=(0,0,0,1)))
        self.code_input =TextInput(size_hint_y =0.1,hint_text ='enter code')
        self.add_widget(self.code_input)
        self.add_widget(Button(text ='submit',size_hint_y=0.1,on_press=self.submit))
        self.add_widget(Label(text ='',size_hint_y=0.6))
        
               
    def paid(self):
        self.clear_widgets()
        self.add_widget(Label(text ='Upgraded',size_hint_y=0.1,color=(0,0,0,1), font_size=30,bold=True))
        lbl=Label(text ='''You are using the upgraded version of this app.
        We appreciate your support and We shall notify you of any new future releases. 
        We wish you all the best while using this app.!''',bold=True, size_hint_y=None,font_size=30,text_size=(Window.size[0] * 0.9, None) ,color=(0,0,0,1),padding=(20,20,20,20))
        self.add_widget(lbl)
        lbl.bind(texture_size=lambda instance, texture_size: setattr(instance, 'height', texture_size[1]))
        self.add_widget(Button(text ='back',on_press=self.admin_page,size_hint_y=0.1))
        self.add_widget(Label(text ='',size_hint_y=0.5))
    def admin_page(self, instance):
        self.clear_widgets()
        self.add_widget(AdminPage(self.logged_in_user))
        
    def submit(self,instance):
        if self.code_input.text!='':
            data=self.db.has_access('has_access' ,code=None)
            if data:
                if self.code_input.text==str(data[0][1]):
                    self.db.update_access('has_access')
                    self.clear_widgets()
                    self.add_widget(MainMenu(self.logged_in_user))
                else:
                    pop_msg('wrong code ','Enter the correct code')
            else:
                pop_msg('code not found','Your request was not processed! you need Internet connection and bundle of about 1mb and try again')
        

class Database:
    def __init__(self, db_list):
        self.connections = {}
        self.cursors = {}
        for db_name in db_list:
            self.connections[db_name] = sqlite3.connect(db_name)
            self.cursors[db_name] = self.connections[db_name].cursor()
            #self.cursors[db_name].execute("PRAGMA foreign_keys = ON;")
            self.create_tables(db_name)

    def create_tables(self, db_name):
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS stock_details(
            stock_details_id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            product_id INTEGER,
            stock_id INTEGER,
            quantity INTEGER,
            cost_price REAL          
        )''')
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS account_recovery(
        account_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        recovery_code INTEGER NOT NULL) ''')
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS company_name(
        company_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        company_name TEXT NOT NULL)''')
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS company_logo(
        image_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        image_path TEXT NOT NULL)''')

        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS stock(
            stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_date DATETIME
        )''')
        
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS other_income(
            income_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            income_date DATETIME DEFAULT (strftime('%Y-%m-%d','now'))
        )''')
        
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS closing_balance(
            bal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            closing_amount REAL, 
            closing_date DATETIME DEFAULT (strftime('%Y-%m-%d','now'))
        )''')
        
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS exp(
            exp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT, 
            amount REAL, 
            exp_date DATETIME DEFAULT ( strftime('%Y-%m-%d','now'))
        )''')

        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_names TEXT,
            email TEXT,
            security_level INTEGER DEFAULT 0,
            password TEXT
        )''')

        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_price REAL NOT NULL,
            min_quantity INTEGER 
        )''')

        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS sales (
            sales_id INTEGER PRIMARY KEY AUTOINCREMENT,            
            sales_date DATETIME,
            user_id INTEGER
        )''')

        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS sales_details (
            sales_details_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            sales_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1
        )''')
        
        self.cursors[db_name].execute('''CREATE TABLE IF NOT EXISTS has_access(
        access_id INTEGER PRIMARY KEY, 
        security_code INTEGER,
        joined_date DATETIME)''')

        self.connections[db_name].commit()
        
    def add_company_name(self,db_name, name):
        self.cursors[db_name].execute('''INSERT INTO company_name(company_name) VALUES(?)''',(name,))
        self.connections[db_name].commit()
        
    def add_account_recovery_code(self, db_name, code):
        self.cursors[db_name].execute('SELECT * FROM account_recovery')
        data=self.cursors[db_name].fetchall()
        if len(data)<1:
            self.cursors[db_name].execute('INSERT INTO account_recovery(recovery_code) VALUES(?)',(code,))
            self.connections[db_name].commit()
            
    def update_account_recovery(self,db_name,code):
        self.cursors[db_name].execute('UPDATE account_recovery SET recovery_code=? WHERE account_id=?',(code,1))
        self.connections[db_name].commit()
        
        
    def get_account_recovery(self,db_name):
        self.cursors[db_name].execute('SELECT * FROM account_recovery')
        return self.cursors[db_name].fetchall()
        
    def update_company_name(self,db_name,name):
        self.cursors[db_name].execute('UPDATE company_name SET company_name=? WHERE company_id=?',(name,1))
        self.connections[db_name].commit()
         
    def add_company_logo(self,db_name, path):
        self.cursors[db_name].execute('''INSERT INTO company_logo(image_path) VALUES(?)''',(path,))
        self.connections[db_name].commit()
        
    def update_company_logo(self,db_name,path):
        self.cursors[db_name].execute('UPDATE company_logo SET image_path=? WHERE image_id=?',(path,1))
        self.connections[db_name].commit()
        
    def get_company_name(self,db_name):
        self.cursors[db_name].execute('SELECT * FROM company_name')
        return self.cursors[db_name].fetchone()
        
    def get_company_logo(self,db_name):
        self.cursors[db_name].execute('SELECT * FROM company_logo')
        return self.cursors[db_name].fetchone() 
          
    def has_access(self,db_name,code=None,access=False):
        self.cursors[db_name ].execute('SELECT * FROM has_access')
        data =self.cursors[db_name].fetchall()
        if code:
            if len(data)==0:
                self.cursors[db_name].execute('INSERT INTO has_access(access_id, security_code,joined_date) VALUES (?,?,?)',(1,code,datetime.today().date().strftime('%Y-%m-%d')))
                self.connections[db_name].commit()
                
            
        else:
            return data
            
    def  update_access(self,db_name):
        self.cursors[db_name].execute('UPDATE has_access SET security_code=? WHERE access_id=?',(0,1))
        self.connections[db_name].commit() 
    
    def delete_sale(self, db_name, sales_id):
        self.cursors[db_name[0]].execute('DELETE FROM sales WHERE sales_id=?',(sales_id, ))
        self.connections[db_name[0]].commit()
        self.cursors[db_name[1]].execute('DELETE FROM sales_details WHERE sales_id=?',(sales_id, ))
        self.connections[db_name[1]].commit()
        
         
    def delete_sale_details(self, db_name, sales_id):
        self.cursors[db_name].execute('DELETE FROM sales_details WHERE sales_details_id=?',(sales_id, ))
        self.connections[db_name].commit() 
        
    def add_stock_details(self,db_name, stock_id, product_id, quantity, price,):
        self.cursors[db_name ].execute('INSERT INTO stock_details(stock_id, product_id, quantity, cost_price) VALUES (?,?,?,?)',(stock_id, product_id, quantity, price))
        self.connections[db_name].commit()
        
    def add_exp(self,db_name, descn, amount):
        self.cursors[db_name ].execute('INSERT INTO exp(description, amount) VALUES (?,?)',(descn,amount))
        self.connections[db_name].commit()
        
    def get_exp(self, db_name, date):
        self.cursors[db_name].execute('SELECT * FROM exp WHERE exp_date=?',(date, ))
        return  self.cursors[db_name].fetchall() 
        
    def add_other_income(self,db_name, descn, amount):
        self.cursors[db_name ].execute('INSERT INTO other_income(description, amount) VALUES (?,?)',(descn, amount))
        self.connections[db_name].commit()
        
    def get_other_income(self, db_name, date):
        self.cursors[db_name].execute('SELECT * FROM other_income WHERE income_date=?',(date, ))
        return  self.cursors[db_name].fetchall()
        
    def all_other_incomes(self, db_name):
        self.cursors[db_name].execute('SELECT * FROM other_income')
        return self.cursors[db_name].fetchall() 
        
        
    def edit_quantity(self,db_name,id,qty):
        self.cursors[db_name].execute('UPDATE sales_details SET quantity=? WHERE sales_details_id =?',(qty,id))
        self.connections[db_name].commit()
        
    def add_closing_balance(self, db_name,amount,date=None):
        if date:
            self.cursors[db_name].execute('INSERT INTO closing_balance(closing_amount,closing_date) VALUES(?,?)',(amount,date))
            self.connections[db_name].commit()
        else:
            self.cursors[db_name].execute('INSERT INTO closing_balance(closing_amount) VALUES(?)',(amount,))
            self.connections[db_name].commit()
        
    def get_closing_balance(self, db_name, date):
        self.cursors[db_name].execute('SELECT closing_amount FROM closing_balance WHERE bal_id = (SELECT MAX(bal_id) FROM closing_balance WHERE closing_date < ?) ', (date,))
        return self.cursors[db_name].fetchone()
        
    def all_closing_balances(self, db_name):
        self.cursors[db_name].execute('SELECT * FROM closing_balance')
        return self.cursors[db_name].fetchall() 
        
    def check_closing_date(self, db_name, date):
        self.cursors[db_name].execute('SELECT bal_id FROM closing_balance WHERE closing_date =?',(date,))
        return self.cursors[db_name].fetchone()
        
        
    def delete_closing_bal(self,db_name,date):
        self.cursors[db_name].execute('DELETE FROM closing_balance WHERE closing_date =?',(date,))
        self.connections[db_name].commit() 
        
        
    def update_bal(self, db_name,id, amount):
        self.cursors[db_name].execute('UPDATE closing_balance SET closing_amount=? WHERE bal_id=?',(amount, id))
        self.connections[db_name].commit()
        
    def get_stock_details(self, db_name, stock_id):
        self.cursors[db_name].execute('SELECT * FROM stock WHERE stock_id=?',(stock_id, ))
        return  self.cursors[db_name].fetchone()
        
        
    def all_purchases(self,db_name):    
        self.cursors[db_name].execute('SELECT * FROM stock ORDER BY stock_id DESC')
        return self.cursors[db_name].fetchall()
          
    def add_stock(self, db_name):
        self.cursors[db_name].execute('INSERT INTO stock (purchase_date) VALUES(?)',(datetime.today().date().strftime('%Y-%m-%d'),))
        self.connections[db_name].commit()
        
    def product_stock(self, db_name):
        # Fetch all product IDs
        self.cursors[db_name[0]].execute('SELECT product_id FROM products')
        products = self.cursors[db_name[0]].fetchall()
        product_ids = [prod[0] for prod in products]
    
        # Fetch sales quantities
        self.cursors[db_name[1]].execute('SELECT product_id, SUM(quantity) FROM sales_details GROUP BY product_id')
        sales = dict(self.cursors[db_name[1]].fetchall())
    
        # Fetch stock quantities
        self.cursors[db_name[2]].execute('SELECT product_id, SUM(quantity) FROM stock_details GROUP BY product_id')
        stock = dict(self.cursors[db_name[2]].fetchall())
    
        # Initialize dictionary with (0, 0) as default values
        result = {prod_id: (0, 0) for prod_id in product_ids}
    
        # Update sales quantities
        for prod_id, sale_qty in sales.items():
            if prod_id in result:
                result[prod_id] = (sale_qty, result[prod_id][1])
    
        # Update stock quantities
        for prod_id, stock_qty in stock.items():
            if prod_id in result:
                result[prod_id] = (result[prod_id][0], stock_qty)
    
        # Sort dictionary by product_id
        result = dict(sorted(result.items()))
    
        return result
    
    def sales_btn_dates(self, db_name, starting_date, ending_date=None):
        if ending_date is None:
            ending_date = datetime.today().date().strftime('%Y-%m-%d')
        starting_date = starting_date.strftime('%Y-%m-%d')
        self.cursors[db_name[1]].execute('SELECT sales_id FROM sales WHERE sales_date>=? AND sales_date<=?', (starting_date, ending_date))
        sales_id = self.cursors[db_name[1]].fetchall()
        sales_ids = tuple(sale[0] for sale in sales_id)
        placeholders = ','.join('?' * len(sales_ids))
        query = 'SELECT product_id, SUM(quantity) AS total_quantity FROM sales_details WHERE sales_id IN (%s) GROUP BY product_id' % placeholders
        self.cursors[db_name[0]].execute(query, sales_ids)
        return self.cursors[db_name[0]].fetchall()
        
    def purchase_btn_dates(self, db_name, starting_date, ending_date=None):
        if ending_date is None:
            ending_date = datetime.today().date().strftime('%Y-%m-%d')
        starting_date = starting_date.strftime('%Y-%m-%d')
        self.cursors[db_name[0]].execute('SELECT stock_id FROM stock WHERE purchase_date>=? AND purchase_date<=?', (starting_date, ending_date))
        sales_id = self.cursors[db_name[0]].fetchall()
        sales_ids = tuple(sale[0] for sale in sales_id)
        placeholders = ','.join('?' * len(sales_ids))
        query = 'SELECT product_id, SUM(quantity) AS total_quantity,AVG(cost_price) AS ave_price FROM stock_details WHERE stock_id IN (%s) GROUP BY product_id' % placeholders
        self.cursors[db_name[1]].execute(query, sales_ids)
        return self.cursors[db_name[1]].fetchall()
            
        
    def purchased_today(self, db_name, date):
        self.cursors[db_name[0]].execute("SELECT * FROM stock WHERE purchase_date=?", (date,))
        purc = self.cursors[db_name[0]].fetchall()
        purc_ids = tuple(pur[0] for pur in purc)
        placeholders = ','.join('?' * len(purc_ids))
        query = 'SELECT product_id, SUM(quantity)AS total_quantity,AVG(cost_price) AS ave_price FROM stock_details WHERE stock_id IN (%s) GROUP BY product_id' % placeholders
        self.cursors[db_name[1]].execute(query, purc_ids)
        return self.cursors[db_name[1]].fetchall()   
                   
            
    def given_stock_id(self, db_name, stock_id):
        self.cursors[db_name].execute('SELECT * FROM stock_details WHERE stock_id=?',(stock_id, ))
        return self.cursors[db_name].fetchall()
        
    def given_sales_id(self, db_name, stock_id):
        self.cursors[db_name].execute('SELECT * FROM sales WHERE sales_id=?',(stock_id, ))
        return self.cursors[db_name].fetchone()    
        
    def last_stock_id(self, db_name ):
        self.cursors[db_name].execute('SELECT stock_id FROM stock ORDER BY stock_id DESC')
        return  self.cursors[db_name].fetchone()

    def new_sale(self, db_name,user_id):
        self.cursors[db_name].execute("INSERT INTO sales(sales_date,user_id)  VALUES(?,?)",(datetime.today().date().strftime('%Y-%m-%d'), user_id)) 
        sales_id = self.cursors[db_name].lastrowid
        self.connections[db_name].commit()
        return self.cursors[db_name].fetchall()

    def make_sales(self, db_name, product_data, sales_id):
        for product_id, quantity in product_data:
             self.cursors[db_name].execute(
                "INSERT INTO sales_details (sales_id, product_id, quantity) VALUES (?, ?, ?)",
                (sales_id, product_id, quantity)
            )
        self.connections[db_name].commit()

    def today_sales(self, db_name, date):
        self.cursors[db_name[1]].execute("SELECT * FROM sales WHERE sales_date=?", (date,))
        sales = self.cursors[db_name[1]].fetchall()
        sales_ids = tuple(sale[0] for sale in sales)
        placeholders = ','.join('?' * len(sales_ids))
        query = 'SELECT product_id, SUM(quantity) AS total_quantity FROM sales_details WHERE sales_id IN (%s) GROUP BY product_id' % placeholders
        self.cursors[db_name[0]].execute(query, sales_ids)
        return self.cursors[db_name[0]].fetchall()
    

    def today_date(self,db_name):
        self.cursors[db_name].execute('SELECT * FROM sales ORDER BY sales_id DESC')
        return self.cursors[db_name].fetchall()
        

    def last_sale(self, db_name):
        self.cursors[db_name].execute('SELECT sales_id FROM sales ORDER BY sales_id DESC')
        return self.cursors[db_name].fetchone()

    def add_products(self, db_name, product_name, product_price, min_qty):
        self.cursors[db_name].execute('''INSERT INTO products (product_name, product_price,min_quantity) VALUES (?,?,?)''', (product_name, product_price,min_qty))
        self.connections[db_name].commit()

    def get_products(self, db_name):
        self.cursors[db_name].execute('SELECT * FROM products')
        return self.cursors[db_name].fetchall()
        
    def update_products(self,db_name,id, name=None, price =None,min_qty=None):
        if name:
            self.cursors[db_name].execute('UPDATE products SET product_name=? WHERE product_id=?',(name,id))
            self.connections[db_name].commit()
        if price:
            self.cursors[db_name].execute('UPDATE products SET product_price=? WHERE product_id=?',(price,id))
            self.connections[db_name].commit()
        if min_qty:
            self.cursors[db_name].execute('UPDATE products SET min_quantity=? WHERE product_id=?',(min_qty,id))
            self.connections[db_name].commit()
    

    def get_sales_details(self, db_name, sales_id):
        self.cursors[db_name].execute('SELECT * FROM sales_details WHERE sales_id=?', (sales_id,))
        return self.cursors[db_name].fetchall()

    def selected_product(self, db_name, product_id):
        self.cursors[db_name].execute('SELECT * FROM products WHERE product_id=?', (product_id,))
        return self.cursors[db_name].fetchone()

         

    def get_product_id(self, db_name, name):
        self.cursors[db_name].execute( 'SELECT product_id FROM products WHERE product_name=?', (name,))
        return self.cursors[db_name].fetchone()
    
    def add_users(self, db_name, username, full_names,email, password,security=None):
        if security:
            if security!='':
                self.cursors[db_name].execute( '''INSERT INTO users (username, full_names, email,security_level,password) VALUES (?,?,?,?,?)''', (username.lower(), full_names.lower(),email.lower(),security,password))
                self.connections[db_name].commit()
            else:
                self.cursors[db_name].execute( '''INSERT INTO users (username, full_names, email,security_lavel,password) VALUES (?,?,?,?,?,?)''', (username.lower(), full_names.lower(),email.lower(),0,password))
                self.connections[db_name].commit()
        else:
            self.cursors[db_name].execute( '''INSERT INTO users (username, full_names, email,security_level,password) VALUES (?,?,?,?,?)''', (username.lower(), full_names.lower(),email.lower(),0,password))
            self.connections[db_name].commit()
     
    def get_user_info(self, db_name):
        self.cursors[db_name].execute( 'SELECT * FROM users')
        return self.cursors[db_name].fetchall()
    
    def get_last_user_id(self, db_name):
        self.cursors[db_name].execute( 'SELECT user_id FROM users ORDER BY user_id DESC')
        return self.cursors[db_name].fetchone()
    
    def get_last_user_info(self, db_name):
        self.cursors[db_name].execute( 'SELECT * FROM users ORDER BY user_id DESC')
        return self.cursors[db_name].fetchone()
    
    def update_user_info(self, db_name, user_id, username=None, full_names=None, security_level=None, password=None,email=None):
        if username:
            self.cursors[db_name].execute( 'UPDATE users set username=? WHERE user_id=?', (username.lower(), user_id))
            self.connections[db_name].commit()
        if full_names:
           self.cursors[db_name].execute( 'UPDATE users set full_names=? WHERE user_id=?', (full_names.lower(), user_id))
           self.connections[db_name].commit()
        if security_level:
            self.cursors[db_name].execute('UPDATE users set security_level=? WHERE user_id=?', (security_level, user_id))
            self.connections[db_name].commit()
        if password:
            self.cursors[db_name].execute('UPDATE users set password=? WHERE user_id=?', (password, user_id))
            self.connections[db_name].commit()
        if email:
            self.cursors[db_name].execute('UPDATE users set email=? WHERE user_id=?', (email.lower(), user_id))
            self.connections[db_name].commit()
    
    def log_in(self, db_name, username, password):
        self.cursors[db_name].execute('SELECT user_id from users WHERE username=? and password=?', (username, password))
        return self.cursors[db_name].fetchone()
        
    def get_user_id(self,db_name, username):
        self.cursors[db_name].execute('SELECT * FROM users WHERE username=?',(username,))
        return self.cursors[db_name].fetchone()
        
    def get_user_details(self,db_name, id):
        self.cursors[db_name].execute('SELECT * FROM users WHERE user_id=?',(id,))
        return self.cursors[db_name].fetchone()
   
             
class IncomeAndExpenses(GridLayout):
    def __init__(self,logged_in_user,income=None, exp=None, **kwargs):
        super(IncomeAndExpenses,self).__init__(**kwargs)
        self.cols=1
        self.logged_in_user =logged_in_user 
        self.selected_date =datetime.today().date().strftime('%Y-%m-%d')
        top = GridLayout(cols=3, size_hint_y=0.07)
        top.add_widget(Button(text='Main Menu', on_press=self.main_menu))
        self.other_btn=Button(text='Go to Expenses page', on_press=self.income_page)
        top.add_widget(self.other_btn)
        top.add_widget(Button(text='Go to Summary page', on_press=self.sales_report))     
        self.add_widget(top)
        self.title=Label(text ='Income Entry',font_size=25,size_hint_y=0.05,bold=True,color=(0,0,0,1))
        self.add_widget(self.title)
        self.income_text='Please include all the amount of money that enters your business which is not from the products you sell. This may include Opening capital or any other income from other sources'
        self.exp_text='Please include all the amount of money that goes out of your business .This may include Lunch,rent,bills,transport etc.'
        self.label=Label(text=self.income_text,text_size=(Window.size[0],None),size_hint_y=0.1,color=(0,0,0,1),padding=(20,20,20,20),font_size=25,bold=True)
        
        self.add_widget(self.label)
        self.grid=GridLayout(cols =2,size_hint_y =0.15)
        self.income_name='Income Description'
        self.income_label=Label(text=self.income_name,size_hint_x=0.4, color=(0,0,0,1),bold=True)
        self.grid.add_widget(self.income_label)
        self.income_input=TextInput(size_hint_x =0.6)
        self.grid.add_widget(self.income_input)
        self.grid.add_widget(Label(text='Amount', size_hint_x=0.4, bold=True, font_size=25, color=(0,0,0,1)))
        self.amount=TextInput(size_hint_x =0.6,input_filter='int')
        self.grid.add_widget(self.amount)
        self.grid.add_widget(Label(text='',size_hint_x=0.4))
        self.submit_btn=Button(text='Add income', size_hint_x=0.6, on_press=self.add_others)
        self.grid.add_widget(self.submit_btn)
        self.add_widget(self.grid)
        header=GridLayout(cols =3,size_hint_y=0.05)
        header.add_widget(Label(text ='',size_hint_x=0.1))
        self.header_name=Button(background_color='green',size_hint_x=0.45)
        header.add_widget(self.header_name)
        header.add_widget(Button(background_color='green',size_hint_x=0.45,text='Amount'))
        self.add_widget(header)
        self.scroll=ScrollView(size_hint_y =0.58)
        self.layout=GridLayout(cols =1,size_hint_y =None )
        self.layout.bind(minimum_height =self.layout.setter('height'))
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
        Clock.schedule_once(lambda dt:self.call_income(dt,income,exp),0)
        
  
    def sales_report(self, instance):
        self.clear_widgets()
        self.add_widget(SalesReport(self.logged_in_user))
        
    def income_page(self, instance):
        if instance.text!='Go to Expenses page':
            self.clear_widgets()
            self.add_widget(IncomeAndExpenses(self.logged_in_user,income=True))
        else:
            self.clear_widgets()
            self.add_widget(IncomeAndExpenses(self.logged_in_user,exp=True))

    def add_income(self,my_list):
          self.layout.clear_widgets()
          total=0
          for row in my_list:
              grid=GridLayout(cols =3,size_hint_y =None, height =70)
              num=my_list.index(row)+1
              grid.add_widget(TextInput(text=str(num),size_hint_x=0.1))
              grid.add_widget(TextInput(text =row[1],size_hint_x=0.45))
              grid.add_widget(TextInput(text =str(row[2]),size_hint_x=0.45))
              total+=row[2]
              self.layout.add_widget(grid)
          total_amount=GridLayout(cols =2,size_hint_y =None, height =70)
          total_amount.add_widget(Label(text ='Total',size_hint_x =0.55,color=(0,0,0,1), bold=True, font_size=30))
          total_amount.add_widget(TextInput(text=str(total), size_hint_x=0.45))
          self.layout.add_widget(total_amount)
          
    def income_data(self):
        db = Database(['other_income.db'])
        data = db.get_other_income('other_income.db', self.selected_date)
        self.add_income(data)
        self.income_label.text='Income description' 
        self.label.text=self.income_text
        self.other_btn.text='Go to Expenses page'
        self.title.text='Income Entry'
        self.header_name.text='Income Description'
        
    def main_menu(self,instance):
        self.clear_widgets()
        self.add_widget(MainMenu(self.logged_in_user))
        
    def exp_data(self):
        db = Database(['exp.db'])
        data = db.get_other_income('exp.db', self.selected_date)
        self.add_income(data)
        self.income_label.text='Expense description' 
        self.other_btn.text='Go to Income page'    
        self.label.text=self.exp_text
        self.submit_btn.text='Add Expense'
        self.title.text='Expense Entry'
        self.header_name.text='Expense Description'
        
    def call_income(self,dt,income,exp):
        if income:
            self.income_data()
        if exp:
            self.exp_data()  
        
    def add_others(self,instance):
        if self.amount.text!='' and self.income_input.text!='':
            if instance.text!='Add Expense':
                db = Database(['other_income.db'])
                db.add_other_income('other_income.db', self.income_input.text, self.amount.text)
                self.income_input.text = ''
                self.amount.text = ''
                self.income_data()
            else:
                db = Database(['exp.db'])
                db.add_other_income('exp.db', self.income_input.text, self.amount.text)
                self.amount.text = ''
                self.income_input.text = ''
                self.exp_data()
    
class SalesReport(GridLayout):
    def __init__(self, logged_in_user, date=None, **kwargs):
        super(SalesReport, self).__init__(**kwargs)
        self.cols = 1
        self.logged_in_user = logged_in_user
        self.selected_date = date or datetime.today().strftime('%Y-%m-%d')

        # Layout containers
        self.home_grid = RelativeLayout()
        self.add_widget(self.home_grid)

        self.layout = GridLayout(cols=1)
        self.home_grid.add_widget(self.layout)

        self.setup_top_menu()
        self.layout.add_widget(Label(
            text='Sales Report', font_size=45, bold=True,
            color=(0, 0, 1, 1), size_hint_y=0.07
        ))
        self.other_layout =GridLayout(cols =1,size_hint_y =0.07)
        self.date_display=Label(text =str(self.selected_date),color =(0,0,0,1),bold =True, font_size=30,size_hint_y=0.07)
        self.other_layout.add_widget(self.date_display)
        self.layout.add_widget(self.other_layout)
        self.setup_summary_section(self.layout)
        self.block = GridLayout(cols=1, size_hint_y=None)
        self.block.bind(minimum_height=self.block.setter('height'))
        self.scroll = ScrollView(size_hint_y=0.49)
        self.layout.add_widget(self.scroll)
        self.scroll.add_widget(self.block)

        self.load_main_block()

    def setup_top_menu(self):
        top = GridLayout(cols=4,size_hint_y=0.07)
        top.add_widget(Button(text='Main Menu', on_press=self.main_menu))
        top.add_widget(Button(text='Add Other Income', on_press=self.go_to_income))
        top.add_widget(Button(text='Add Expenses', on_press=self.go_to_exp))
        top.add_widget(Button(text='Search Record\nfor Different Date', on_press=self.search_block))
        self.layout.add_widget(top)

    def search_block(self, instance):
        self.other_layout.clear_widgets()
        self.t = 0
        self.flash_grid = GridLayout(cols=2, size_hint_y=None, height=70)
        date_grid = RelativeLayout(size_hint_x=0.6)
        self.date_input = TextInput(hint_text='Enter date to search')
        date_grid.add_widget(self.date_input)
        date_grid.add_widget(Button(text='', opacity=0, on_press=self.open_calendar))
        self.flash_grid.add_widget(date_grid)
        self.flash_grid.add_widget(Button(text='Search', size_hint_x=0.4, on_press=self.search_record))
        self.flash_clock = Clock.schedule_interval(self.flash, 0.03)
    
    def flash(self, dt):
        self.t += 1
        if self.t % 2 == 0:
            self.other_layout.add_widget(self.flash_grid)
        else:
            if self.flash_grid in self.other_layout.children:
                self.other_layout.remove_widget(self.flash_grid)
        if self.t >= 8:  
            Clock.unschedule(self.flash_clock)
            if self.flash_grid not in self.other_layout.children:
                self.other_layout.add_widget(self.flash_grid)
        
    def go_to_income(self,instance):
        self.clear_widgets()
        self.add_widget(IncomeAndExpenses(self.logged_in_user, income=True))
        
    def go_to_exp(self,instance):
        self.clear_widgets()
        self.add_widget(IncomeAndExpenses(self.logged_in_user,exp=True))

    def open_calendar(self, instance):
        pop = Popup(size_hint_y=None, height=500, size_hint_x=None, width=600, title='Select date')
        cal = CalendarWidget(on_date_selected=lambda date: (self.handle_selected_date(date), pop.dismiss()))
        pop.content = cal
        pop.open()

    def handle_selected_date(self, date):
        self.date_input.text = str(date)

    def search_record(self, instance):
        if not self.date_input.text:
            return
        try:
            dates = datetime.strptime(self.date_input.text, '%Y-%m-%d')
            formatted_date = dates.strftime('%Y-%m-%d')
            db = Database(['closing_balance.db'])
            id = db.check_closing_date('closing_balance.db', formatted_date)
            if id:
                self.clear_widgets()
                self.add_widget(SalesReport(self.logged_in_user, date=formatted_date))
            else:
                pop_msg('No record', f'There were no records for {formatted_date}')
        except ValueError:
            pop_msg('Invalid date', 'Please enter the date in YYYY-MM-DD format.')

    def load_main_block(self):
        self.main_block()
        
    def main_block(self):
        block = GridLayout(cols=1, size_hint_y=None)
        block.bind(minimum_height =block.setter('height') )
        self.block.add_widget(block)

        self.my_incomes = GridLayout(cols=1,size_hint_y=None)
        self.my_incomes.bind(minimum_height=self.my_incomes.setter('height'))
        self.my_exp = GridLayout(cols=1, size_hint_y=None)
        self.my_exp.bind(minimum_height=self.my_exp.setter('height'))

        
        block.add_widget(self.my_incomes)
        self.income_grid()
        block.add_widget(self.my_exp)
        self.exp_grid()
        #self.all_closing_balances(block)

    def setup_summary_section(self, parent):
        bal = ClosingBalances(date=self.selected_date)
        layout=GridLayout(cols =2,size_hint_y =0.3)
        grid = GridLayout(cols=2, size_hint_y=None)
        grid.bind(minimum_height =grid.setter('height'))
        def summary_row(label, value, color=(0, 0, 0, 1), font_size=35, bg_color=None):
            layout.add_widget(Label(text=label, size_hint_x=0.4, bold=True, font_size=font_size, color=color))
            txt = TextInput(text=str(value), size_hint_x=0.6, font_size=font_size, readonly=True)
            if bg_color:
                txt.background_color = bg_color
            layout.add_widget(txt)

        summary_row('Opening Balance', bal.get_amount(opening_amount=1))
        summary_row('Total Sales', bal.get_amount(sales_amount=1))
        summary_row('Other Income', bal.get_amount(income_amount=1))
        summary_row('Total Expenses', bal.get_amount(exp_amount=1))
        summary_row('Total Purchases', bal.get_amount(stock_amount=1))
        summary_row('Total Cash', bal.get_amount(closing_amount=1), color=(0, 0, 1, 1), font_size=50, bg_color=(1, 1, 0, 1))
        parent.add_widget(layout)

    def main_menu(self, instance):
        self.clear_widgets()
        self.add_widget(MainMenu(self.logged_in_user))

    def add_others(self, instance):
        if self.income_desn.text and self.amount.text:
            db = Database(['other_income.db'])
            db.add_other_income('other_income.db', self.income_desn.text, self.amount.text)
            self.income_desn.text = ''
            self.amount.text = ''
            self.income_grid()

    def add_exp(self, instance):
        if self.exp_desn.text and self.exp_amount.text:
            db = Database(['exp.db'])
            db.add_other_income('exp.db', self.exp_desn.text, self.exp_amount.text)
            self.exp_desn.text = ''
            self.exp_amount.text = ''
            self.exp_grid()

    def income_grid(self):
        self.my_incomes.clear_widgets()
        self.my_incomes.add_widget(Label(text='Other Income', size_hint_y=None, height=70, bold=True, font_size=40, color=(0,0,0,1)))
        db = Database(['other_income.db'])
        data = db.get_other_income('other_income.db', self.selected_date)
        total = 0
        for row in data:
            if row:
                layout = GridLayout(cols=2, size_hint_y=None, height=70)
                layout.add_widget(TextInput(text=row[1], font_size=40, readonly=True, size_hint_x=0.4, height=70))
                layout.add_widget(TextInput(text=f'{row[2]:,}', font_size=40, readonly=True, size_hint_x=0.6, height=70))
                self.my_incomes.add_widget(layout)
                total += row[2]
        self.my_incomes.add_widget(self.summary_line('Total Income', total, (1, 0.3, 0.6, 1)))

    def exp_grid(self):
        self.my_exp.clear_widgets()
        self.my_exp.add_widget(Label(text='Expenses', size_hint_y=None, height=70, bold=True, font_size=40,color=(0,0,0,1)))
        db = Database(['exp.db'])
        data = db.get_other_income('exp.db', self.selected_date)
        total = 0
        for row in data:
            if row:
                layout = GridLayout(cols=2, size_hint_y=None, height=70)
                layout.add_widget(TextInput(text=row[1], font_size=40, readonly=True, size_hint_x=0.4, height=70))
                layout.add_widget(TextInput(text=f'{row[2]:,}', font_size=40, readonly=True, size_hint_x=0.6, height=70))
                self.my_exp.add_widget(layout)
                total += row[2]
        self.my_exp.add_widget(self.summary_line('Total Expenses', total, (0.5, 0.2, 0.6, 1)))

    def summary_line(self, label, total, bg_color):
        line = GridLayout(cols=2, size_hint_y=None, height=70)
        line.add_widget(TextInput(text=label, font_size=40, readonly=True, size_hint_x=0.4, background_color=bg_color, foreground_color=(1, 1, 1, 1)))
        line.add_widget(TextInput(text=f'{total:,}', font_size=40, readonly=True, size_hint_x=0.6, background_color=bg_color, foreground_color=(1, 1, 1, 1)))
        return line

    def all_closing_balances(self, parent):
        db = Database(['closing_balance.db'])
        data = db.all_closing_balances('closing_balance.db')
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for row in data:
            layout = GridLayout(cols=3, size_hint_y=None, height=70)
            layout.add_widget(TextInput(text=str(row[0]), readonly=True))
            layout.add_widget(TextInput(text=str(row[1]), readonly=True))
            layout.add_widget(TextInput(text=row[2], readonly=True))
            grid.add_widget(layout)
        parent.add_widget(grid)
          
class ClosingBalances:
    def __init__(self, date=None):
        self.selected_date = date or datetime.today().strftime('%Y-%m-%d')
        self.closing_bal = self.calculate_closing_balance()

        # Automatically update or add today's record
        if self.selected_date == datetime.today().strftime('%Y-%m-%d'):
            db = Database(['closing_balance.db'])
            record = db.check_closing_date('closing_balance.db', self.selected_date)
            if record:
                db.update_bal('closing_balance.db', record[0], self.closing_bal)
            else:
                db.add_closing_balance('closing_balance.db', self.closing_bal)

    def calculate_closing_balance(self):
        return (
            self.get_opening_balance() +
            self.get_sales() +
            self.get_income() -
            self.get_expenses() -
            self.get_purchases()
        )

    def get_opening_balance(self):
        db = Database(['closing_balance.db'])
        bal = db.get_closing_balance('closing_balance.db', self.selected_date)
        return bal[0] if bal else 0  # index 1 = closing_amount

    def get_sales(self):
        db = Database(['sales_details.db', 'sales.db', 'products.db'])
        sales_data = db.sales_btn_dates(['sales_details.db', 'sales.db', 'products.db'], datetime.strptime(self.selected_date, '%Y-%m-%d'))
        product_db = Database(['products.db'])
        total = 0
        for row in sales_data or []:
            product = product_db.selected_product('products.db', row[0])
            total += product[2] * row[1]  # price * quantity
        return total

    def get_purchases(self):
        db = Database(['stock.db', 'stock_details.db', 'products.db'])
        purchases = db.purchase_btn_dates(['stock.db', 'stock_details.db', 'products.db'], 
                                          datetime.strptime(self.selected_date, '%Y-%m-%d'),
                                          ending_date=datetime.strptime(self.selected_date, '%Y-%m-%d'))
        return sum(row[2] * row[1] for row in purchases or [])  # price * quantity

    def get_income(self):
        db = Database(['other_income.db'])
        data = db.get_other_income('other_income.db', self.selected_date)
        return sum(row[2] for row in data or [])

    def get_expenses(self):
        db = Database(['exp.db'])
        data = db.get_other_income('exp.db', self.selected_date)
        return sum(row[2] for row in data or [])

    def get_amount(self, opening_amount=False, sales_amount=False, income_amount=False, 
                   exp_amount=False, stock_amount=False, closing_amount=False):
        if opening_amount:
            return self.get_opening_balance()
        if sales_amount:
            return self.get_sales()
        if income_amount:
            return self.get_income()
        if exp_amount:
            return self.get_expenses()
        if stock_amount:
            return self.get_purchases()
        if closing_amount:
            return self.closing_bal
        return 0
               
class StockBalance(GridLayout):
    def __init__(self,logged_in_user,low_stock=None,**kwargs):
        
        super(StockBalance,self).__init__(**kwargs)
        self.logged_in_user=logged_in_user
        self.cols=1
        top_btn =GridLayout(cols =3,size_hint_y =0.07)
        top_btn.add_widget(Button(text='MainMenu',on_press=self.main_menu))
        top_btn.add_widget(Button(text='All products stock',on_press=self.all_products))
        top_btn.add_widget(Button(text='Low Quantity Products',on_press=self.low_products))
        self.add_widget(top_btn)
        self.add_widget(Label(text ='Stock Table',size_hint_y=0.1,color=(0,0,1,1),bold=True, font_size=60))
        head=GridLayout(cols =6,size_hint_y=0.07)
        head.add_widget(Label(text ='',size_hint_x=0.1))
        head.add_widget(Button(text='Product',background_color='green',bold=True,size_hint_x=0.25))
        
        head.add_widget(Button(text='Minimun\nQuantity',background_color='green',bold=True,size_hint_x=0.15))
        head.add_widget(Button(text='Total\n Purchase',background_color='green', bold=True,size_hint_x=0.15))
        head.add_widget(Button(text='Total\nSales',background_color='green', bold=True,size_hint_x=0.15))
        head.add_widget(Button(text='Actual\n Stock',background_color='green', bold=True,size_hint_x=0.16))
        self.add_widget(head)
        scroll=ScrollView(size_hint_y =0.76)
        self.layout=GridLayout(cols =1,size_hint_y =None )
        
        self.layout.bind(minimum_height =self.layout.setter('height'))
        scroll.add_widget(self.layout)
        self.add_widget(scroll)
        if low_stock:
            self.low_stock()
        else:
            self.my_table()
        
    def main_menu(self,instance):
        self.clear_widgets()
        self.add_widget(MainMenu(self.logged_in_user))
        
    def all_products(self,instance):
        self.clear_widgets()
        self.add_widget(StockBalance(self.logged_in_user))
     
    def low_products(self,instance):
        self.clear_widgets()
        self.add_widget(StockBalance(self.logged_in_user,low_stock=True))     
     
    def low_stock(self):    
        self.layout.clear_widgets()
        db = Database(['products.db', 'sales_details.db', 'stock_details.db'])
        data = db.product_stock(['products.db', 'sales_details.db', 'stock_details.db'])
        db2 = Database(['products.db'])
    
        count = 1  # Counter for visible rows only
        for row in data:
            name = db2.selected_product('products.db', row)
            total_qty = data[row][1] - data[row][0]
    
            if total_qty <= name[3]:
                layout = GridLayout(cols=6, size_hint_y=None, height=70)
    
                no = TextInput(text=str(count), size_hint_x=0.1, readonly=True)
                layout.add_widget(no)
    
                prod = TextInput(text=str(name[1]), size_hint_x=0.25, height=70, readonly=True)
                layout.add_widget(prod)
    
                min_qty = TextInput(text=str(name[3]), size_hint_x=0.16, height=70, readonly=True)
                layout.add_widget(min_qty)
    
                sale = TextInput(text=str(data[row][1]), size_hint_x=0.16, height=70, readonly=True)
                layout.add_widget(sale)
    
                purc = TextInput(text=str(data[row][0]), size_hint_x=0.16, height=70, readonly=True)
                layout.add_widget(purc)
    
                total = TextInput(
                    text=str(total_qty),
                    size_hint_x=0.17,
                    height=70,
                    background_color=(1, 0.7, 0.8, 1),
                    readonly=True,
                    foreground_color=(0, 0, 0, 1),
                    font_size=30
                )
                layout.add_widget(total)
    
                self.layout.add_widget(layout)
                count += 1  # Increment only when a row is added
                      
    def my_table(self):
        self.layout.clear_widgets()
        db = Database(['products.db', 'sales_details.db', 'stock_details.db'])
        data = db.product_stock(['products.db', 'sales_details.db', 'stock_details.db'])
        db2 = Database(['products.db'])
    
        for idx, row in enumerate(data):
            name = db2.selected_product('products.db', row)
            layout = GridLayout(cols=6, size_hint_y=None, height=70)
    
            total_qty = data[row][1] - data[row][0]
            low_stock = total_qty <= name[3]
    
            # Numbering
            no = TextInput(text=str(idx + 1), size_hint_x=0.1, readonly=True)
            if low_stock:
                no.background_color = (1, 0.5, 0.5, 1)  # Light red
            layout.add_widget(no)
    
            prod = TextInput(text=str(name[1]), size_hint_x=0.25, height=70, readonly=True)
            if low_stock:
                prod.background_color = (1, 0.5, 0.5, 1)
            layout.add_widget(prod)
    
            min_qty = TextInput(text=str(name[3]), size_hint_x=0.16, height=70, readonly=True)
            if low_stock:
                min_qty.background_color = (1, 0.5, 0.5, 1)
            layout.add_widget(min_qty)
    
            sale = TextInput(text=str(data[row][1]), size_hint_x=0.16, height=70, readonly=True)
            if low_stock:
                sale.background_color = (1, 0.5, 0.5, 1)
            layout.add_widget(sale)
    
            purc = TextInput(text=str(data[row][0]), size_hint_x=0.16, height=70, readonly=True)
            if low_stock:
                purc.background_color = (1, 0.5, 0.5, 1)
            layout.add_widget(purc)
    
            total = TextInput(
                text=str(total_qty),
                size_hint_x=0.17,
                height=70,
                readonly=True,
                font_size=30,
                foreground_color=(0, 0, 0, 1),
                background_color=(1,1,1,1) if not low_stock else (1, 0.3, 0.3, 1)
            )
            layout.add_widget(total)
    
            self.layout.add_widget(layout)
            
            

class LogIn(GridLayout):
    def __init__(self,**kwargs ):
        super(LogIn,self).__init__(**kwargs)
        self.cols=1
        self.block=GridLayout(cols =2,size_hint_y=0.3)
        self.step =0
        self.code=random.randint(100000,999999)
        label=Label(text='Welcome to Dñ Bŕüñõvîç Sales App.',size_hint_y=None,bold=True,text_size=(Window.size[0],None),color=(0,0,0,1),font_size=30, padding=(20,20,20,20))   
        label.bind(texture_size=lambda instance, texture_size: setattr(instance, 'height', texture_size[1])) 
        self.add_widget(label)
        self.add_widget(Label (text ='Login to continue',size_hint_y=0.1,font_size=38,bold=True, color=(0,0,0,1)))
        self.block.add_widget(Label(text ='Username',bold=True, font_size=25,size_hint_x=0.4, color=(0,0,0,1)))
        self.username_entry =TextInput(size_hint_x =0.6)
        self.block.add_widget(self.username_entry)
        self.block.add_widget(Label(text ='password',size_hint_x=0.4,font_size=25,bold=True, color=(0,0,0,1)))
        self.password_entry = TextInput(size_hint_x=0.6, password=True)
        self.block.add_widget(self.password_entry)
        btn=RelativeLayout(size_hint_x =0.4)
        
        btn.add_widget(Label(text ="Forgot password?",bold=True, color=(0,0,1,1)))
        btn.add_widget(Button(text ='',opacity=0.2,on_press=self.account_recovery))
        self.block.add_widget(btn)
        self.block.add_widget(Button(text ='Login',on_press=self.log_in))
        self.add_widget(self.block)
        self.add_widget(Label(text ='',size_hint_y=0.5))
        
    def account_recovery(self,instance):
        db=Database(['users.db'])
        self.clear_widgets()
        self.add_widget(Label(text ='Account Recovery',bold=True, font_size=30,color=(0,0,0,1),size_hint_y=0.2))
        grid=GridLayout(cols =2,size_hint_y=0.2)
        self.recovery_grid=GridLayout(cols =1,size_hint_x=0.6)
        self.label=Label(text ='enter username',size_hint_x=0.4, bold=True, color=(0,0,0,1))
        grid.add_widget(self.label)
        self.name=TextInput()
        self.email=TextInput()
        self.code_input=TextInput()
        self.new_password=TextInput()
        self.reenter_password=TextInput()
        grid.add_widget(self.recovery_grid)
        self.recovery_grid.add_widget(self.name)
        self.back_btn=Button(text ='Cancel',size_hint_x=0.4,on_press=self.back_button)
        grid.add_widget(self.back_btn)
        grid.add_widget(Button(text ='Next',size_hint_x=0.6,on_press=self.recovery_logic))
        self.add_widget(grid)
        self.add_widget(Label(text ='',size_hint_y=0.6))
        
    def refresh(self,instance):
        self.clear_widgets()
        self.add_widget(LogIn())
        
    def recovery_logic(self, instance):
        users = Database(['users.db'])
        if self.step == 0:
            if self.name.text != '':
                user = users.get_user_id('users.db', self.name.text.lower())
                if user:
                    if user[4] == 1:
                        self.recovery_grid.clear_widgets()
                        self.recovery_grid.add_widget(self.email)
                        self.label.text = 'Enter Your Email'
                        self.step = 1
                        self.back_btn.text='Back'
                    else:
                        pop_msg('Access denied', f'Please ask anyone else with admin access to update your password under user info')
                else:
                    pop_msg('invalid username', 'Username not found')
        elif self.step == 1:
            user = users.get_user_id('users.db', self.name.text.lower())
            if self.email.text != '':
                if self.email.text.lower() == user[3]:
                    my_send_mail('Account Recovery', f'your recovery code is {self.code} do not share it with any one else.', self.email.text, logic=lambda: self.add_code())
                    self.step = 2
                else:
                    pop_msg('Access denied', 'Email Address does not match')
        elif self.step == 2:
            if self.code_input.text != '':
                if self.code_input.text == str(self.code):
                    self.recovery_grid.clear_widgets()
                    self.recovery_grid.add_widget(self.new_password)
                    self.label.text = 'Enter New password'
                    self.step = 3
                else:
                    pop_msg('invalid code', 'code does not match ' + str(self.code))
        elif self.step == 3:
            if self.new_password.text != '':
                self.recovery_grid.clear_widgets()
                self.recovery_grid.add_widget(self.reenter_password)
                instance.text = 'Finish'
                self.label.text = 're_enter password'
                self.step = 4
        elif self.step == 4:
            if self.reenter_password.text != '':
                if self.new_password.text == self.reenter_password.text:
                    users.update_user_info('users.db', users.get_user_id('users.db', self.name.text.lower())[0], password=self.new_password.text)
                    pop_msg('success', 'Your password is updated successfully')
                    self.clear_widgets()
                    self.add_widget(LogIn())

    def back_button(self, instance):
        if instance.text == 'Cancel':
            self.clear_widgets()
            self.add_widget(LogIn())
        else:
            if self.step > 0:
                self.step -= 1
                if self.step == 0:
                    self.recovery_grid.clear_widgets()
                    self.recovery_grid.add_widget(self.name)
                    self.back_btn.text='Cancel'
                    self.label.text = 'Enter Your username'
                elif self.step == 1:
                    self.recovery_grid.clear_widgets()
                    self.recovery_grid.add_widget(self.email)
                    self.label.text = 'Enter Your Email'
                elif self.step == 2:
                    self.recovery_grid.clear_widgets()
                    self.recovery_grid.add_widget(self.code_input)
                    self.label.text = 'Enter code sent\non your email'
                elif self.step == 3:
                    self.recovery_grid.clear_widgets()
                    self.recovery_grid.add_widget(self.new_password)
                    self.label.text = 'Enter new password'
            
            
    def add_code(self):
        self.recovery_grid.clear_widgets()
        self.recovery_grid.add_widget(self.code_input)
        self.label.text ='Enter code sent\non your email'  
        
              
    def log_in(self,instance):
        if self.username_entry.text!='' and self.password_entry.text!='':
            db=Database(['users.db'])
            user=db.log_in('users.db',self.username_entry.text, self.password_entry.text)
            if user:
                self.clear_widgets()
                self.add_widget(CheckSubscription(user[0]))
            else:
                pop_msg('invalid details','invalid username or password')
                
    def signup(self, instance):
        self.clear_widgets()
        self.add_widget(SignUp())
                
                
class SignUp(GridLayout):
    def __init__(self,**kwargs ):
        super(SignUp,self).__init__(**kwargs)
        self.cols=1
        self.block=GridLayout(cols =2,size_hint_y=0.4)
        label=Label(text='Welcome to Dñ Bŕüñõvîç Sales App', size_hint_y=0.1,font_size=34,bold=True, color=(0,0,0,1),padding=(20,0,0,20))
        self.code=random.randint(100000,999999)
        self.add_widget(label)
        self.add_widget(Label (text ='Register to continue',size_hint_y=0.1,font_size=38,bold=True, color=(0,0,0,1)))
        self.block.add_widget(Label(text ='Full Names',bold=True, size_hint_x=0.4, color=(0,0,0,1)))
        self.full_names_entry =TextInput(size_hint_x =0.6)
        self.block.add_widget(self.full_names_entry)
        self.block.add_widget(Label(text ='Username',bold=True, font_size=25,size_hint_x=0.4, color=(0,0,0,1)))
        self.username_entry =TextInput(size_hint_x =0.6)
        self.block.add_widget(self.username_entry)
        self.block.add_widget(Label(text ='Email_address',bold=True, font_size=25,size_hint_x=0.4, color=(0,0,0,1)))
        self.email_entry =TextInput(size_hint_x =0.6)
        self.block.add_widget(self.email_entry)
        self.block.add_widget(Label(text ='password',size_hint_x=0.4,font_size=25,bold=True, color=(0,0,0,1)))
        self.password_entry =TextInput(size_hint_x=0.6, password=True)
        self.block.add_widget(self.password_entry)
        self.block.add_widget(Label(text ='confirm password',size_hint_x=0.4,font_size=25,bold=True, color=(0,0,0,1)))
        self.re_enter_password_entry =TextInput(size_hint_x=0.6, password=True)
        self.block.add_widget(self.re_enter_password_entry)
        btn=RelativeLayout(size_hint_x =0.4)
        
        btn.add_widget(Label(text ="Aready have account?",bold=True, color=(0,0,1,1),))
        btn.add_widget(Button(text ='',opacity=0.2,on_press=self.log_in))
        self.block.add_widget(btn)
        self.block.add_widget(Button(text ='Sign up',on_press=self.submit_details))
        self.add_widget(self.block)
        self.add_widget(Label(text ='',size_hint_y=0.4))
        
    def submit_details(self, instance):
        
        if self.full_names_entry.text!='' and self.username_entry.text!='' and self.password_entry.text!='' and self.re_enter_password_entry.text!='' and self.email_entry.text!='':
            if self.password_entry.text ==self.re_enter_password_entry.text:
                db=Database(['users.db'])
                user=db.get_user_id('users.db',self.username_entry.text)
                if not user:
                    my_send_mail('Complete SignUp',f'Yello {self.full_names_entry. text}! please complete signing up using {self.code} as your verification code.\n Do not share it with any one else.\nIf you are getting this email by accident please ignore. \nRegards Dñ Bŕûñõvîç sales App.',self.email_entry.text,logic=lambda :self.get_code())
                    
                    
                else:
                    pop_msg('username exists','user name already exists please user a different username')
            else:
                pop_msg("passwords don't match",'your passwords do not match')
        else:
            pop_msg('empty fields','please fill in all the fields')
            
    def get_code(self):
        self.clear_widgets()
        self.add_widget(Label(text ='Complete SignUp', font_size=34,bold=True, size_hint_y=0.1, color=(0,0,0,1)))
        self.add_widget(Label(text ='please enter the verification code sent on your email',size_hint_y=0.1, color=(0,0,0,1), font_size=20))
        grid =GridLayout(cols =2,size_hint_y =0.2)
        grid.add_widget(Label(text ='Enter code',bold=True, font_size=20,size_hint_x=0.4, color=(0,0,0,1)))
        self.code_input =TextInput(size_hint_x =0.6 )
        grid.add_widget(self.code_input)
        grid.add_widget(Button(text ='Back',on_press=self.reload,size_hint_x=0.4))
        grid.add_widget(Button(text ='Submit',on_press=self.finish,size_hint_x=0.6))
        self.add_widget(grid)
        self.add_widget(Label(text ='',size_hint_y=0.6))
         
         
    def reload(self ,instance):
        self.clear_widgets()
        self.add_widget(SignUp())
            
    def finish(self,instance):
        if self.code_input.text==str(self.code):
            db=Database(['users.db'])
            db.add_users('users.db',self.username_entry.text,self.full_names_entry.text,self.email_entry.text,self.password_entry.text,security=1)
            
            self.clear_widgets()
            self.add_widget(LogIn())
            has=Database(['has_access'])
            data=has.has_access('has_access',code=None)
        
            if data:
                pass
            else:
                send_code()
        else:
           pop_msg('invalid code','code does not match ')
           
    def log_in(self, instance):
        self.clear_widgets()
        self.add_widget(LogIn())
            
            
                
class SalesPage(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
        super(SalesPage, self).__init__(**kwargs)
        self.cols=1
        self.logged_in_user =logged_in_user 
        self.users=Database(['users.db'])
        self.logged_in_username=self.users.get_user_details('users.db',self.logged_in_user)[1]
        self.sales_checkbox=[]
        self.sales_rows=[]
        self.warning_layout=RelativeLayout(size_hint_y =None, height =350,size_hint_x =None, width =400,pos_hint={'x':0.3, 'y':0.5})
        self.options_widget = GridLayout(cols=3, size_hint_y=None, height=50, pos_hint={'y': 0.5})
        self.options_widget.add_widget(Button(text='Delete selection',background_color='red',on_press=lambda instance:self.warning_msg(instance, 'delete selected records','delete',self.delete_record)))
        self.options_widget.add_widget(Button(text='Edit quantity',background_color='green',on_press=self.enable_editing))
        self.options_widget.add_widget(Button(text='Clear all',background_color='maroon',on_press=lambda instance :self.warning_msg(instance, 'clear all this sale details','clear' ,self.clear_sales)))
        
        self.block=GridLayout(cols =1,on_touch_down=lambda instance, touch:self.remove_options(instance,touch,self.options_widget))
        top_btn=GridLayout(cols=4,size_hint_y=0.07)      
        top_btn.add_widget(Button(text ='main menu',on_press=self.main_menu))
        top_btn.add_widget(Button(text ='New sale',on_press=self.new_record))
        top_btn.add_widget(Button(text ='Today sales',on_press=lambda instance :self.total_sales_display(instance,datetime.today().date())))
        db=Database(['sales.db'])
        values=db.today_date('sales.db')
        self.spinner=Spinner(text ='Search sales',values=[str(val[0]) for val in values])
        top_btn.add_widget(self.spinner)
        self.spinner.bind(text=self.selected_sale)
        self.block.add_widget(top_btn)
        self.title_label_grid=GridLayout(cols=1,size_hint_y=0.07)
        self.title_label=Label(text ='Sales page',font_size=60,color=(0,0,1,1), bold=True)
        self.sales_btn=GridLayout(cols =3)
        self.sales_btn.add_widget(Label(text ='',size_hint_x=0.2))
        self.sales_btn.add_widget(Button(text ='Search Sales Of Different Dates',on_press=self.open_date_layout, size_hint_x=0.6))
        self.sales_btn.add_widget(Label(text ='',size_hint_x=0.2))
        self.title_label_grid.add_widget(self.title_label)
        self.block.add_widget(self.title_label_grid)
        self.home_block=RelativeLayout()
        self.home_block.add_widget(TextInput(disabled =True ))
        self.home_block.add_widget(self.block)
        self.add_widget(self.home_block)
        self.sales_layout=ScrollView(size_hint_y =0.49 )
        self.input_layout=GridLayout(cols =1,size_hint_y=0.3)
        self.block.add_widget(self.input_layout)
       
        self.sales_grid=GridLayout(cols =1,size_hint_y =None )
        self.sales_grid.bind(minimum_height =self.sales_grid.setter('height'))
        self.sales_layout.clear_widgets()
        self.sales_layout.add_widget(self.sales_grid)
        
        self.sales_input()
        self.sales_label()
        self.block.add_widget(self.sales_layout)
        self.add_sales()
        
        
    def open_date_layout(self,instance):
         self.title_label_grid.clear_widgets()
         grid=GridLayout(cols =3)
         start_grid=RelativeLayout()
         self.start_date=TextInput(hint_text ='Start Date')
         start_grid.add_widget(self.start_date)
         start_grid.add_widget(Button(text='',opacity=0,on_press=lambda instance :self.open_calendar(instance, self.start_date)))
         grid.add_widget(start_grid)
         end_grid=RelativeLayout()
         
         self.end_date=TextInput(hint_text ='End Date')
         end_grid.add_widget(self.end_date)
         end_grid.add_widget(Button(text='',opacity=0,on_press=lambda instance :self.open_calendar(instance, self.end_date)))
         grid.add_widget(end_grid)
         grid.add_widget(Button(text='Search',on_press=lambda instance:self.total_sales_display(instance,self.start_date.text,end_date=self.end_date.text)))
         self.title_label_grid.add_widget(grid)
         

    def sales_label(self):
        
        head = GridLayout(cols=5, size_hint_y=0.07)
        btn_list =[]
        labs = ['', 'product name', 'quantity', 'Price', 'Amount']
    
        for lb in labs:
           
            col = RelativeLayout()
            col.add_widget(Button(background_color='yellow', text='',))
            col.add_widget(Label(text=lb,bold=True, font_size=25, color=(0,0,0,1)))
            btn_list.append(col)
            head.add_widget(col)
            
        btn_list[0].size_hint_x =0.1
        btn_list[0].opacity =0
        btn_list[1].size_hint_x =0.25
        btn_list[2].size_hint_x =0.2
        btn_list[3].size_hint_x =0.2
        btn_list[4].size_hint_x =0.25
        self.block.add_widget(head)
        
    def new_record(self,instance):
        self.my_new_record()
        
    def my_new_record(self):
        self.title_label_grid.clear_widgets()
        self.title_label_grid.add_widget(self.title_label)
        self.title_label.text='Sales page'
        self.input_layout.clear_widgets()
        self.input_layout.size_hint_y =0.3
        self.input_layout.opacity=1
        self.title_label_grid.size_hint_y =0.07
        if self.input_box not in self.input_layout.children:
            self.input_layout.add_widget(self.input_box)
            self.sales_layout.scroll_y=0.49
        self.sales_grid.clear_widgets()
        self.name_disp.text =self.logged_in_username
        
        self.sales_disp.text =''
        self.search_btn.text=''
        self.quantity_input.text=''
        
    def main_menu(self, instance ):
        self.block.clear_widgets()
        self.block.add_widget(MainMenu(self.logged_in_user))
        
    def sales_input(self ):  
        
        scr=ScrollView( size_hint=(None, None),height=800,width=350,pos_hint={'x':0.5,'y':0.3})
        self.floated = FloatLayout()
        self.input_layout.clear_widgets()
        search_results_layout = GridLayout(cols=1,size_hint_y=None)
        search_results_layout.bind(minimum_height =search_results_layout.setter('height'))
   
        scr.add_widget(search_results_layout)
        
        self.floated.add_widget(scr)
        
        db=Database(['sales.db'])
        self.input_box=GridLayout(cols =2)
        sales_id=db.last_sale('sales.db')
        self.input_box.add_widget(Label(text ='sales date', size_hint_x=0.4, color=(0,0,0,1),bold=True, font_size=35))
        self.date_disp=TextInput(size_hint_x =0.6 ,disabled =True)
        self.input_box.add_widget(self.date_disp)
        self.input_box.add_widget(Label(text ='sales person', size_hint_x=0.4, color=(0,0,0,1),bold=True, font_size=35))
        self.name_disp=TextInput(size_hint_x =0.6 ,disabled =True)
        
        self.input_box.add_widget(self.name_disp)
        self.input_box.add_widget(Label(text ='sales id',size_hint_x=0.4, color=(0,0,0,1),bold=True, font_size=35))
        self.sales_disp=TextInput(size_hint_x=0.6,hint_text='New',disabled=True)
        self.search_btn =SearchInput(self.home_block,self.floated,hint_text='type to search')
        self.search_btn.search_results_layout = search_results_layout
        self.product_id=self.search_btn.product_id
        if sales_id:
            self.sales_disp.text=str(sales_id[0])
            self.date_disp.text =str(db.given_sales_id('sales.db',sales_id[0])[1])
            self.name_disp.text=self.users.get_user_details('users.db',db.given_sales_id('sales.db',sales_id[0])[2])[1]
        self.input_box.add_widget(self.sales_disp)
        self.input_box.add_widget(Label(text ='select product',size_hint_x=0.4,color=(0,0,0,1),bold=True, font_size=35))   
        self.input_box.add_widget(self.search_btn)
        self.input_box.add_widget(Label(text='quantity',size_hint_x=0.4, color=(0,0,0,1), bold=True, font_size=35))
        self.quantity_input=TextInput(size_hint_x=0.6, input_filter='int')
        self.input_box.add_widget(self.quantity_input)
        self.input_box.add_widget(Label (text ='',size_hint_x=0.4))
        self.input_box.add_widget(Button(text ='add',size_hint_x=0.6, on_press=self.add_new_sale))
        self.input_box.add_widget(Button(text ='prev',size_hint_x=None, width=200,on_press=self.switch_sales))
        grid=GridLayout(cols=2)
        grid.add_widget(Button(text ='Next',on_press=self.switch_sales))
        grid.add_widget(Button(text ='Print',on_press=self.generate_receipt))
        self.input_box.add_widget(grid)
        self.input_layout.add_widget(self.input_box)
        
    def add_new_sale(self, instance):
        if self.search_btn.text!='' and self.quantity_input.text!='':
            if self.sales_disp.text != '':
                db2=Database(['products.db'])
                id=db2.get_product_id('products.db',self.search_btn.text)
                db = Database(['sales_details.db'])
                if id:
                    if self.date_disp.text==datetime.today().date().strftime('%Y-%m-%d'):
                        db.make_sales('sales_details.db',[(id[0], int(self.quantity_input.text))], int(self.sales_disp.text))
                        data=Database(['sales.db'])
                        self.add_sales()
                        self.search_btn.text =''
                        self.quantity_input.text=''
                        
                        self.date_disp.text =str(data.given_sales_id('sales.db',int(self.sales_disp.text))[1])
                        ClosingBalances()
                        values=data.today_date('sales.db')
                        self.spinner.values=[str(val[0]) for val in values]
                    else:
                        pop_msg('different date','you cannot add on this sale since its not for today.')
                else:
                    pop_msg('invalid product name', 'product name not found please select from the list or add it to the table in products page first')
                
            else:
                db = Database(['sales.db'])
                
                db2=Database(['products.db'])
                id=db2.get_product_id('products.db',self.search_btn.text)
                if id:
                    db.new_sale('sales.db',self.logged_in_user)
                    self.sales_disp.text = str(db.last_sale('sales.db')[0])
                    db3 = Database(['sales_details.db'])
                    db3.make_sales('sales_details.db', [(id[0], int(self.quantity_input.text))], int(self.sales_disp.text))
                    self.date_disp.text =str(db.given_sales_id('sales.db',int(self.sales_disp.text))[1])
                    values=db.today_date('sales.db')
                    self.spinner.values=[str(val[0]) for val in values]
                    ClosingBalances()
                    self.add_sales()
                    self.search_btn.text = ''
                    self.quantity_input.text = ''
                else:
                    pop_msg('invalid product name', 'product name not found!\n please select from the list or add it to the table in products page first.')
                    
                    
    
        
    def switch_sales(self, instance):
        sales = Database(['sales.db'])
        values = sales.today_date('sales.db')
        sales_ids = [val[0] for val in values]
    
        if self.sales_disp.text.isdigit():
            current_id = int(self.sales_disp.text)
            if current_id in sales_ids:
                idx = sales_ids.index(current_id)
                
                if instance.text == 'prev':
                    idx += 1
                    if idx < len(sales_ids):
                        new_id = sales_ids[idx]
                        self.sales_disp.text = str(new_id)
                        self.date_disp.text = str(sales.given_sales_id('sales.db', new_id)[1])
                        self.add_sales()
                else:
                    idx -= 1
                    if idx >= 0:
                        new_id = sales_ids[idx]
                        self.sales_disp.text = str(new_id)
                        self.date_disp.text = str(sales.given_sales_id('sales.db', new_id)[1])
                        self.add_sales()
                        
                        
    def total_sales_display(self,instance,start_date,end_date=None):
           date_format = '%Y-%m-%d'
           sale_db = Database(['sales_details.db', 'sales.db', 'products.db'])
           today_sales = sale_db.sales_btn_dates(['sales_details.db', 'sales.db', 'products.db'],datetime.strptime(str(start_date), date_format))
           
           if end_date is None:
               self.title_label_grid.clear_widgets()
               self.title_label_grid.add_widget(self.sales_btn)
               self.today_sales(today_sales)
               self.title_label.text='Today Sales'
           else:
               if end_date =='':
                   end_date =str(datetime.today().date())
               self.title_label_grid.clear_widgets()
               self.title_label_grid.add_widget(self.title_label)
               given_sales_date=sale_db.sales_btn_dates(['sales_details.db', 'sales.db', 'products.db'],datetime.strptime(str(start_date),date_format),ending_date=datetime.strptime(end_date,date_format))
               self.today_sales(given_sales_date)
               self.title_label.text=f'Sales from {start_date} - {end_date}'
               self.title_label.font_size=30
          
    def open_calendar(self, instance, ctrl):
        pop = Popup(size_hint_y=None, height=500, size_hint_x=None, width=600, title='Select date')
        cal = CalendarWidget(on_date_selected=lambda date: (self.handle_selected_date(date, ctrl), pop.dismiss()))
        pop.content = cal
        pop.open()
        
        
    def format_amount(self, value):
        if value == int(value):
            return str(int(value))  # 12.0 → "12"
        return f"{value:.2f}".rstrip('0').rstrip('.')  # 12.50 → "12.5", 12.55 → "12.55"
    
    def generate_receipt(self, instance):
        pop = Popup(size=(300, 800), size_hint=(None, None), title='Receipt Preview')
        grid = GridLayout(cols=1)
    
        # Buttons
        btns = GridLayout(cols=2, size_hint_y=0.1)
        btns.add_widget(Button(text='Cancel', on_press=lambda x: pop.dismiss()))
        btns.add_widget(Button(text='Print'))  # Optional: Hook up to Bluetooth print
        grid.add_widget(btns)
    
        # Scrollable label for receipt preview
        scroll = ScrollView(size_hint_y=0.9)
        label = Label(
            font_size=14,
            size_hint_y=None,
            halign='center',
            valign='top',
            text_size=(290, None)
        )
        label.bind(texture_size=self.resize_label)
        scroll.add_widget(label)
        grid.add_widget(scroll)
    
        # Build receipt content
        db = Database(['company_name.db'])
        comp_name = db.get_company_name('company_name.db')
        company = comp_name[1] if comp_name else "SALES RECEIPT"
    
        if self.sales_disp.text != '':
            lines = []
            lines.append(f"  {company}")
            lines.append(f"Date: {self.date_disp.text}   Time: {datetime.now().strftime('%H:%M')}")
            lines.append(f'Sales Id: {int(self.sales_disp.text):04}')
            lines.append("-" * 32)
            lines.append("Item        Qty  Price  Total   ")
            
    
            sales = Database(['sales_details.db'])
            prod = Database(['products.db'])
            my_sales = sales.get_sales_details('sales_details.db', self.sales_disp.text)
    
            total_price = 0
            for row in my_sales:
                if row:
                    product_data = prod.selected_product('products.db', row[1])
                    name = product_data[1][:10]
                    qty = str(row[3])
                    price_val = product_data[2]
                    total_val = float(product_data[2]) * int(row[3])
                    total_price += total_val
                    lines.append(f"{name[:10]:<10}{qty[:2]:>3}{self.format_amount(price_val):>8}{self.format_amount(total_val):>8}")
    
            lines.append("-" * 32)
            lines.append("{:<26}{:>6}".format("Total:", self.format_amount(total_price)))
            lines.append("Thank you for your purchase!")
    
            label.text = "\n".join(lines)
            pop.content = grid
            pop.open()
    
    def resize_label(self, instance, size):
        instance.height = instance.texture_size[1]
        
    def print_receipt(self,instance):
        
        sales = Database(['sales_details.db'])
        prod = Database(['products.db'])
        if self.sales_disp.text!='':
            my_sales=sales.get_sales_details('sales_details.db', (self.sales_disp.text))
            for row in my_sales:
                if row:
                    layout = GridLayout(cols=5, size_hint_y=None, height=80)                      
                    product_data = prod.selected_product('products.db' ,row[1])              
                    product_name =product_data[1]
                    price =str(product_data[2])              
                    quantity = str(row[3])
                    amount =  {float(product_data[2]*int(row[3]))}
                    
        
    def handle_selected_date(self,date,ctrl):
        ctrl.text=str(date)
        
    def today_sales(self,my_list):
        self.input_layout.size_hint_y=0
        
        self.sales_grid.clear_widgets()
        self.sales_layout.size_hint_y=0.75
        self.title_label_grid.size_hint_y=0.07
        self.input_layout.opacity=0
        sales_list =[]
        date_format = datetime.today().date().strftime('%Y-%m-%d')
        
        prod = Database(['products.db'])
        for row in my_list:
            layout = GridLayout(cols=5, size_hint_y = None, height=80)
            product_data = prod.selected_product('products.db' ,row[0])
            check =TextInput(size_hint_x=0.1)
            num=my_list.index(row)+1
           
            check.text=str(num)
                
            layout.add_widget(check)
            product_name=TextInput(size_hint_x =0.25,text=product_data[1])
            layout.add_widget(product_name)
            price=TextInput(text =str(row[1]),size_hint_x =0.2)
            layout.add_widget(price)
            quantity =TextInput(size_hint_x =0.2,text=str(product_data[2]))
            layout.add_widget(quantity)
            amount= TextInput(size_hint_x =0.25)
            layout.add_widget(amount) 
            amount.text=f'ugx. {row[1]*(product_data[2])}' 
            self.sales_grid.add_widget(layout)
            sales_list.append((amount.text))
                    
       
        totals=GridLayout(cols =3,size_hint_y =None, height =80)
        self.sales_grid.add_widget(totals)
        totals.add_widget(Label(text ='',size_hint_x=0.2))
        totals.add_widget(Label(text ='Total',size_hint_x=0.3,bold=True, font_size=40,color=(0,0,0,1)))
        total_input=TextInput(size_hint_x =0.5,readonly=True,font_size=40)
        totals.add_widget(total_input)
        
        total_amount = 0
        
        for tot in sales_list:
            if tot:
                am = tot.replace('ugx.','').strip()
                total_amount += float(am)

        total_input.text = f'ugx. {total_amount}'
        
        
        
    def selected_sale(self,instance,value) :
        sales = Database(['sales.db'])
        if value:
            if value!='Search sales':
                self.sales_disp.text = value
                self.date_disp.text=str(sales.given_sales_id('sales.db',int(value))[1])
                self.add_sales()
                instance.text='Search sales'
                
            
    def add_sales(self):
   
        sales = Database(['sales_details.db'])
        prod = Database(['products.db'])
        self.sales_grid.clear_widgets()
  
        
        self.totals=[]
        # Fetch sales details
        if self.sales_disp.text!='':
            my_sales=sales.get_sales_details('sales_details.db', (self.sales_disp.text))
            self.sale_details(my_sales,prod,self.totals)
            self.totals_layout(self.totals)
            
            
    def edit_quantity(self, instance, value):
        if instance.text =='':
            instance.text ='0'
        if not hasattr(instance, 'initial_text'):
            instance.initial_text = instance.text
        
        if instance.text != instance.initial_text:
            for row in self.sales_rows:
                if instance in row and instance == row[2]:
                    db = Database(['sales_details.db'])
                    db.edit_quantity('sales_details.db', row[0], int(instance.text))
                    self.add_sales()
                    break
                    
                    

    def enable_editing(self, instance):
        selected = [row[1].active for row in self.sales_rows]
        if sum(selected) == 1:
            for row in self.sales_rows:
                if row[1].active:
                    row[2].focus =True 
                    break 
                    
    def warning_msg(self,instance,msg,text,function):
        self.warning_layout.clear_widgets()
        self.warning_layout.add_widget(TextInput(readonly =True, background_color=(0,0,0,1)))
        layout=GridLayout(cols =1)
        layout.add_widget(Label(text ='warning! ',size_hint_y =0.3,font_size=25))
        layout.add_widget(Label(text =f'Are you sure you want to {msg}?\n Remember you cannot Undo!',size_hint_y =None,text_size=(self.warning_layout.width,None),bold=True, font_size=20))
        btn=GridLayout(cols =2,size_hint_y =0.3)
        btn.add_widget(Button(text='Cancel',on_press=self.cancel_warning))
        btn.add_widget(Button(text=text, on_press=function))
        layout.add_widget(btn)
        self.warning_layout.add_widget(layout)
        if self.warning_layout not in self.home_block.children:
            self.home_block.add_widget(self.warning_layout)
    
        
    def cancel_warning(self,instance):
        self.home_block.remove_widget(self.warning_layout)
                
    def remove_options(self,instance,touch,widget):
        if widget  in self.home_block.children:
            if not self.sales_layout.collide_point(*touch.pos):
                self.home_block.remove_widget(widget)
            
            
    def on_status_change(self, instance, value):
            if any(widget.active for widget in self.sales_checkbox):
                if self.options_widget not in self.home_block.children:
                    self.home_block.add_widget(self.options_widget)
            else:
                if self.options_widget in self.home_block.children:
                    self.home_block.remove_widget(self.options_widget)
            
    def delete_record(self,instance):
        db=Database(['sales_details.db'])
        for row in self.sales_rows:
            if row[1].active:
                db.delete_sale_details('sales_details.db',row[0])
                self.add_sales()
        self.home_block.remove_widget(self.warning_layout)
        self.home_block.remove_widget(self.options_widget)   
        
                    
    def clear_sales(self,instance):
        data=Database(['sales.db'])
        db=Database(['sales.db','sales_details.db'])
        db.delete_sale(['sales.db','sales_details.db'] ,int(self.sales_disp.text))
        self.my_new_record()
        self.home_block.remove_widget(self.warning_layout)
        self.home_block.remove_widget(self.options_widget)
        values=data.today_date('sales.db')
        self.spinner.values=[str(val[0]) for val in values]
        
    def sale_details(self,my_sales,prod,list):
        for row in my_sales:
            if row:
                layout = GridLayout(cols=5, size_hint_y=None, height=80)
                        
                product_data = prod.selected_product('products.db' ,row[1])
                if row[2]!='':  # Fetch product details 
                    check = CheckBox( background_checkbox_normal='/storage/emulated/0/DCIM/Screenshots/Screenshot_20250121_234943_Google.jpg',size_hint_x=0.1)
                    self.sales_checkbox.append(check)
                    check.bind(active=lambda instance, value :self.on_status_change(instance, value))
                    layout.add_widget(check)
                
                    product_name = TextInput(size_hint_x=0.25, readonly=True)  # Set product name
                        
                    product_name.text=product_data[1]
                    layout.add_widget(product_name)
                
                    price = TextInput(size_hint_x=0.2, readonly=True,input_filter='int')  # Set product price
                    
                    
                    if product_data:
                        price.text=str(product_data[2])
                
                    quantity = TextInput(size_hint_x=0.2, text=str(row[3]), input_filter='int')  # Set quantity
                    layout.add_widget(quantity)    
                    layout.add_widget(price)
                    self.sales_rows.append((row[0],check,quantity))
                    quantity.bind(focus=self.edit_quantity)
                    amount = TextInput(size_hint_x=0.25,readonly=True)  # Compute amount
                    if product_data:
                        amount.text=(f'ugx.  {float(product_data[2]*int(row[3]))}')
                    layout.add_widget(amount)
                    list.append((amount.text))
                
                    self.sales_grid.add_widget(layout)
                    
                    
    def totals_layout(self,list):                
                        
        totals=GridLayout(cols =3,size_hint_y =None, height =80)
        self.sales_grid.add_widget(totals)
        totals.add_widget(Label(text ='',size_hint_x=0.2))
        totals.add_widget(Label(text ='Total',size_hint_x=0.3,bold=True, font_size=40,color=(0,0,0,1)))
        total_input=TextInput(size_hint_x =0.5,readonly=True,font_size=40)
        totals.add_widget(total_input)
        
        total_amount = 0
        for tot in list:
            if tot:
                am = tot.replace('ugx.','').strip()
                total_amount += float(am)

        total_input.text = f'ugx. {total_amount}'
                

                       
class Stock(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
        super(Stock, self).__init__(**kwargs)
        self.cols=1
        self.logged_in_user =logged_in_user 
        self.block_layout =RelativeLayout()
        self.block_layout.add_widget(TextInput(disabled =True ))
        self.block=GridLayout(cols =1)
        self.add_widget(self.block_layout)
        self.block_layout.add_widget(self.block)
        self.sales_rows=[]
        self.selected_product_id=''
        
        top_btn=GridLayout(cols=4,size_hint_y=0.07, )
        top_btn.add_widget(Button(text ='main menu',on_press=self.main_menu))
        top_btn.add_widget(Button(text ='New stock', on_press=self.go_to_new))
        top_btn.add_widget(Button(text ='Purchased Today',on_press=lambda instance :self.total_purchase_display(instance, datetime.today().date())))
        db=Database(['stock.db'])
        stock_ids=db.all_purchases('stock.db')
        self.spinner =Spinner(text ='Search stock-in',values=[str(val[0]) for val in stock_ids])
        self.spinner.bind(text=self.selected_stock)
        top_btn.add_widget(self.spinner)
        
        self.block.add_widget(top_btn)
        self.title_label_grid=GridLayout(cols =1,size_hint_y =0.07)
        self.title_label=Label(text ='StockIn page', font_size=60,bold=True, color=(0,0,1,1))
        self.title_label_grid.add_widget(self.title_label)
        self.sales_btn =GridLayout(cols =3)
        start_date_grid=RelativeLayout()
        self.start_date =TextInput(hint_text='start date')
        start_date_grid.add_widget(self.start_date)
        start_date_grid.add_widget(Button(text='',opacity=0,on_press=lambda instance:self.open_calendar(instance, self.start_date)))
        self.end_date =TextInput(hint_text='end date')
        self.end_date_grid=RelativeLayout()
        self.end_date_grid.add_widget(self.end_date)
        self.end_date_grid.add_widget(Button(text='',opacity=0,on_press=lambda instance:self.open_calendar(instance, self.end_date)))
        
        self.sales_btn.add_widget(start_date_grid)
        self.sales_btn.add_widget(self.end_date_grid)
        self.sales_btn.add_widget(Button(text ='Search',on_press=lambda instance :self.total_purchase_display(instance, self.start_date. text,end_date=self.end_date.text)))
        self.btns_grid=GridLayout(cols =3)
        self.btns_grid.add_widget(Label(text ='',size_hint_x=0.2))
        self.btns_grid.add_widget(Button(text ='Search purchaces for other days',size_hint_x=0.6,on_press=self.open_date_layout))
        self.btns_grid.add_widget(Label(text ='',size_hint_x=0.2))
        
        
        self.block.add_widget(self.title_label_grid)
        
        self.input_layout=GridLayout(cols =1,size_hint_y=0.3)
        self.block.add_widget(self.input_layout)
        self.stock_input()
        
        self.heading=GridLayout(cols =5,size_hint_y =0.07)
        
        self.heading.add_widget(Label(text ='',size_hint_x=0.1))
        self.heading.add_widget(Label (text ='product name',size_hint_x=0.3, color=(0,0,0,1), font_size=30,bold=True))
        self.heading.add_widget(Label(text ='cost price',size_hint_x=0.2,font_size=30,color=(0,0,0,1), bold=True))
        self.heading.add_widget(Label(text ='quantity',  size_hint_x=0.2, color=(0,0,0,1), font_size=30, bold=True))
        self.heading.add_widget(Label(text ='amount' ,size_hint_x=0.2,font_size=30,color=(0,0,0,1), bold=True))
        self.block.add_widget(self.heading)
        self.sales_layout=ScrollView(size_hint_y =0.49)
        self.block.add_widget(self.sales_layout)
        self.sales_grid=GridLayout(cols =1,size_hint_y =None )
        self.sales_grid.bind(minimum_height =self.sales_grid.setter('height'))
        self.sales_layout.add_widget(self.sales_grid)
        self.add_stock()
        
    def open_date_layout(self, instance):
        self.title_label_grid.clear_widgets()
        self.title_label_grid.add_widget(self.sales_btn)
        
    def stock_input(self ):
        self.layout =GridLayout(cols =2)
        scr=ScrollView( size_hint=(None, None),height=800,width=350,pos_hint={'x':0.5,'y':0.3})
        self.floated = FloatLayout()
        self.input_layout.add_widget(self.layout)
        search_results_layout = GridLayout(cols=1,size_hint_y=None)
        search_results_layout.bind(minimum_height =search_results_layout.setter('height'))
       
        scr.add_widget(search_results_layout)
        
        self.floated.add_widget(scr)
        self.layout.clear_widgets()
        db=Database(['stock.db'])
        stock_id=db.last_stock_id('stock.db')
        self.layout.add_widget(Label(text ='stock date',size_hint_x=0.4 ,bold=True, font_size=30,color=(0,0,0,1)))
        self.date_input=TextInput(size_hint_x=0.6,disabled=True)
        self.layout.add_widget(self.date_input)
        self.layout.add_widget(Label(text ='stock id',size_hint_x=0.4, bold=True,font_size=30,color=(0,0,0,1)))
        self.stock_disp=TextInput(size_hint_x=0.6,disabled=True,hint_text='New')
        if self.stock_disp.text!='':
            db=Database(['stock.db'])
            date=db.get_stock_details('stock.db',int(self.stock_disp.text))
            self.date_input.text=date[1]
        self.search_btn =SearchInput(self.block_layout,self.floated, hint_text='type to search', size_hint_x=0.6)
        self.search_btn.search_results_layout = search_results_layout
        self.product_id=self.search_btn.product_id
        if stock_id:
            self.stock_disp.text=str(stock_id[0])       
        self.layout.add_widget(self.stock_disp)
        self.layout.add_widget(Label(text ='select product',size_hint_x=0.4,bold=True, color=(0,0,0,1), font_size=30))        
        self.layout.add_widget(self.search_btn)
        self.layout.add_widget(Label(text='quantity',size_hint_x=0.4, bold=True, font_size=30,color=(0,0,0,1)))
        self.quantity_input =TextInput (size_hint_x=0.6,input_filter='int')
        self.layout.add_widget(self.quantity_input)
        self.layout.add_widget(Label(text ='cost price',size_hint_x=0.4,bold=True,font_size=30,color=(0,0,0,1)))
        self.price_entry=TextInput(size_hint_x =0.6, input_filter ='int')
        self.layout.add_widget(self.price_entry)
        
        self.layout.add_widget(Label (text ='',size_hint_x=0.4))
        self.layout.add_widget(Button(text ='add',size_hint_x=0.6, on_press=self.add_new_stock))
        
        
    def main_menu(self,instance):
        self.clear_widgets()
        self.add_widget(MainMenu(self.logged_in_user))
        
    def add_new_stock(self, instance):
        
        if self.stock_disp.text != '':
            db2=Database(['products.db'])
            id=db2.get_product_id('products.db',self.search_btn.text)
            db = Database(['stock_details.db'])
            if id:
                stock=Database(['stock.db'])
                stock_date=stock.get_stock_details('stock.db',int(self.stock_disp.text))[1]
                if str(datetime.today().date())!=str(stock_date):
                    pop_msg('invalid purchase date','You cannot continue to stock on this list! please go to new stock_in.')
                else:
                    db.add_stock_details('stock_details.db',int(self.stock_disp.text),id[0], int(self.quantity_input.text), int(self.price_entry.text))
                    self.add_stock()
                    self.search_btn.text =''
                    self.quantity_input.text=''
                    self.price_entry.text =''
            else:
                pop_msg('invalid product name', 'product name not found!\n please select from the list or add it to the table in products page first.')
        else:
            db = Database(['stock.db'])
            db.add_stock('stock.db')
            db2=Database(['products.db'])
            id=db2.get_product_id('products.db',self.search_btn.text)
            if id:
                self.stock_disp.text = str(db.last_stock_id('stock.db')[0])
                db3 = Database(['stock_details.db'])
                db3.add_stock_details('stock_details.db',int(self.stock_disp.text),id[0], int(self.quantity_input.text), int(self.price_entry.text))
            else:
                pop_msg('invalid product name', 'product name not found!\n please select from the list or add it to the table in products page first.')
              
            
            self.add_stock()
            self.search_btn.text = ''
            self.quantity_input.text = ''
            self.price_entry.text =''
        
    def total_purchase_display(self,instance,start_date,end_date=None):
           date_format = '%Y-%m-%d'
           sale_db = Database(['stock.db', 'stock_details.db', 'products.db'])
           today_sales = sale_db.purchase_btn_dates(['stock.db', 'stock_details.db', 'products.db'],datetime.strptime(str(start_date), date_format))
           
           if end_date is None:
               
               self.title_label_grid.clear_widgets()
               self.title_label_grid.add_widget(self.btns_grid)
               self.today_stock(today_sales)
               self.title_label.text='Today Sales'
           else:
               if end_date =='':
                   end_date=str(datetime.today().date())
               self.title_label_grid.clear_widgets()
               self.title_label_grid.add_widget(self.title_label)
               given_sales_date=sale_db.purchase_btn_dates(['stock.db', 'stock_details.db', 'products.db'],datetime.strptime(start_date,date_format),ending_date=datetime.strptime(end_date,date_format))
               self.today_stock(given_sales_date)
               self.title_label.text=f'Sales from ({start_date}) - ({end_date})'
               self.title_label.font_size=30      
               
    def today_stock(self,my_list):
        self.input_layout.size_hint_y=0
        self.title_label.text ='Purchased Today'
        self.sales_grid.clear_widgets()
        self.sales_layout.size_hint_y=0.79
        self.input_layout.clear_widgets()
        sales_list =[]
        date_format = datetime.today().date().strftime('%Y-%m-%d')
        
        prod = Database(['products.db'])
        for row in my_list:
            layout = GridLayout(cols=5, size_hint_y = None, height=80)
            product_data = prod.selected_product('products.db' ,row[0])
            check =TextInput(size_hint_x=0.1)
            num=my_list.index(row)+1
           
            check.text=str(num)
                
            layout.add_widget(check)
            product_name=TextInput(size_hint_x =0.25,text=product_data[1])
            layout.add_widget(product_name)
            price=TextInput(text =str(row[1]),size_hint_x =0.2)
            layout.add_widget(price)
            quantity =TextInput(size_hint_x =0.2,text=str(row[2]))
            layout.add_widget(quantity)
            amount= TextInput(size_hint_x =0.25)
            layout.add_widget(amount) 
            amount.text=f'ugx. {row[1]*row[2]}' 
            self.sales_grid.add_widget(layout)
            sales_list.append((amount.text))
                    
       
        totals=GridLayout(cols =3,size_hint_y =None, height =80)
        self.sales_grid.add_widget(totals)
        totals.add_widget(Label(text ='',size_hint_x=0.2))
        totals.add_widget(Label(text ='Total',size_hint_x=0.3,bold=True, font_size=40,color=(0,0,0,1)))
        total_input=TextInput(size_hint_x =0.5,readonly=True,font_size=40)
        totals.add_widget(total_input)
        
        total_amount = 0
        
        for tot in sales_list:
            if tot:
                am = tot.replace('ugx.','').strip()
                total_amount += float(am)

        total_input.text = f'ugx. {total_amount}'  
        
        
    
    def open_calendar(self, instance, ctrl):
        pop = Popup(size_hint_y=None, height=500, size_hint_x=None, width=600, title='Select date')
        cal = CalendarWidget(on_date_selected=lambda date: (self.handle_selected_date(date, ctrl), pop.dismiss()))
        pop.content = cal
        pop.open()
        
    def handle_selected_product(self,product_id):
        self.selected_product_id=product_id
             
    def handle_selected_date(self,date,ctrl):
        ctrl.text=str(date)     
        
    def selected_stock(self, instance, value):
        db=Database(['stock.db'])
        if value:
            if value!='Search stock-in':
                self.stock_disp.text =value
                self.date_input.text=str(db.get_stock_details('stock.db',int(value))[1])
                self.add_stock()
                instance.text='Search stock-in'
        
    def stock_table(self,instance) :
        self.sales_grid.clear_widgets()
        stock =Database(['stock.db'])
        data=stock.today_stock('stock.db')
        for row in data:
            layout=GridLayout(cols =2,size_hint_y=None, height=80)
            layout.add_widget(TextInput(text =str(row[0])))
            layout.add_widget(TextInput(text =row[1]))
            self.sales_grid.add_widget(layout)
            
    def go_to_new(self,instance):
        self.title_label_grid.clear_widgets()
        self.title_label_grid.add_widget(self.title_label)
        self.title_label.font_size=60
        self.title_label.text ='Stock In page'
        self.sales_layout.size_hint_y=0.49
        self.input_layout.size_hint_y =0.3
        if self.layout not in self.input_layout.children:
            self.input_layout.add_widget(self.layout)
        self.sales_grid.clear_widgets()
        
        self.stock_disp.text =''
        self.search_btn.text =''
        self.price_entry.text=''
        self.quantity_input.text =''
        self.date_input.text =str(datetime.today().date())
        
            
    def add_stock(self):
        stock = Database(['stock_details.db'])
        prod = Database(['products.db'])
        self.sales_grid.clear_widgets()
        self.totals=[]
        # Fetch sales details
        if self.stock_disp.text!='':
            my_sales=stock.given_stock_id('stock_details.db', int(self.stock_disp.text))
            self.sale_details(my_sales,prod,self.totals)
            self.totals_layout(self.totals)
            
    def sale_details(self,my_sales,prod,list):
        for row in my_sales:
            if row:
                layout = GridLayout(cols=5, size_hint_y=None, height=80)
                        
                product_data = prod.selected_product('products.db' ,row[1])
                if row[2]!='':  # Fetch product details 
                    check = CheckBox(size_hint_y=None, height=80, background_checkbox_normal='/storage/emulated/0/DCIM/Screenshots/Screenshot_20250121_234943_Google.jpg',size_hint_x=0.1)
                    layout.add_widget(check)
                
                    product_name = TextInput(size_hint_x=0.3,readonly=True)  # Set product name
                        
                    product_name.text=product_data[1]
                    layout.add_widget(product_name)
                
                    price = TextInput(size_hint_x=0.2, readonly=True)  # Set product price
                    layout.add_widget(price)
                    if product_data:
                        price.text=str(row[4])
                
                    quantity = TextInput(size_hint_x=0.2, text=str(row[3]))  # Set quantity
                        
                    layout.add_widget(quantity)
                
                    amount = TextInput(size_hint_x=0.2,readonly=True)  # Compute amount
                    if product_data:
                        amount.text=(f'ugx.  {float(row[4]*int(row[3]))}')
                    layout.add_widget(amount)
                    list.append((amount.text))
                
                    self.sales_grid.add_widget(layout)
                    
                    
    def totals_layout(self,list):                
                        
        totals=GridLayout(cols =3,size_hint_y =None, height =80)
        self.sales_grid.add_widget(totals)
        totals.add_widget(Label(text ='',size_hint_x=0.2))
        totals.add_widget(Label(text ='Total',size_hint_x=0.3,bold=True, font_size=40))
        total_input=TextInput(size_hint_x =0.5,readonly=True,font_size=40)
        totals.add_widget(total_input)
        
        total_amount = 0
        for tot in list:
            if tot:
                am = tot.replace('ugx.','').strip()
                total_amount += float(am)

        total_input.text = f'ugx. {total_amount}'
        
        
                       
class SearchInput(TextInput):
    def __init__(self, manager, wid,product_id=None, **kwargs):
        super(SearchInput, self).__init__(**kwargs)
        self.manager = manager  
        self.wid = wid  
        self.product_id = product_id  
        self.db = Database(['products.db'])  
        self.search_results_layout = None  # This will be set externally
        self.bind(text=self.on_text)  # Bind text change event

    def on_text(self, instance, value):
        items = self.db.get_products('products.db')
        search_results = [item for item in items if value.lower() in item[1].lower()]  

        # Ensure search_results_layout exists before modifying it
        if self.search_results_layout:
            self.search_results_layout.clear_widgets()

        if value and search_results:
            # Ensure the results are displayed
            self.manager.remove_widget(self.wid)
            self.manager.add_widget(self.wid)

            for item in search_results:
                btn = Button(
                    text=item[1],  # Display product name
                    background_color=(0.5, 0.5, 0.5, 1),
                    size_hint=(None, None),
                    width=300,
                    height=100,
                )
                # Correct lambda function for passing both text and product ID
                btn.bind(on_press=lambda instance, prod_id=item[0],prod_name=item[1]: 
                         self.selected_product_id(prod_id, prod_name))
                self.search_results_layout.add_widget(btn)

        elif not search_results:
            self.manager.remove_widget(self.wid)
            label = Label(text="No results found", size_hint=(None, None), width=300, height=50)
            self.search_results_layout.add_widget(label)

        else:
            self.manager.remove_widget(self.wid)

    def selected_product_id(self, product_id,product_name):
        if self.product_id:
       
            self.product_id(product_id)
        self.text = product_name # Set input text to selected product name

        # Hide results
        if self.search_results_layout:
            self.search_results_layout.clear_widgets()
            self.manager.remove_widget(self.wid)
        
            
            
class ProductsPage(GridLayout):
    def __init__(self,logged_in_user,**kwargs):
        super(ProductsPage, self).__init__(**kwargs)
        self.cols=1
        self.logged_in_user =logged_in_user 
        self.block_layout =RelativeLayout()
        self.block =GridLayout(cols=1)
        self.add_widget(self.block_layout)
        self.block_layout.add_widget(TextInput(disabled =True ))
        self.block_layout.add_widget(self.block)
        self.product_rows=[]
        top_btn=GridLayout(cols=3,size_hint_y=0.07)
        top_btn.add_widget(Button(text ='main menu',on_press=self.main_menu))
        top_btn.add_widget(Button(text ='Add new product',on_press=self.add_product_layout))
        top_btn.add_widget(Button(text ='products table',on_press=self.products_data))
        self.block.add_widget(top_btn)
        self.heading=GridLayout(cols =3,size_hint_y =0.07)
        self.block.add_widget(self.heading)
        self.sales_layout=ScrollView(size_hint_y =0.86)
        self.block.add_widget(self.sales_layout)
        self.keyb=Label(text ='',size_hint_y=0)
        self.block.add_widget(self.keyb)
        self.add_products()
        
    def price_on_focus(self, instance,value):
        if value:
            txt = instance.text.replace('Ugx ','')
            val = txt.split('.')
            instance.text = str(val[0])
        else:
            instance.text=f'Ugx {instance.text}.0'
        
    def keyboard_height(self, instance, value):
        self.sales_layout.size_hint_y=0.46
        self.keyb.size_hint_y =0.4
        if value:
            
            layout_height = self.data_block.height
            instance_y = instance.y
            scroll_y = (instance_y+300 - self.sales_layout.height) / (layout_height - self.sales_layout.height)
            Animation.cancel_all(self.sales_layout, 'scroll_y')
            self.sales_layout.scroll_y = scroll_y
        else:
            self.sales_layout.size_hint_y =0.86
            self.keyb.size_hint_y =0
            
    def add_product_layout(self, instance):
          
       self.sales_layout.clear_widgets()
       self.add_products()
           
    def main_menu(self, instance):
        self.clear_widgets()
        self.add_widget(MainMenu(self.logged_in_user))
        
    def update_products(self,instance, value):
       db=Database(['products.db'])
       if value:
           for row in self.product_rows:
               if instance in row:
                   if row[1]==instance:
                     
                       db.update_products('products.db', int(row[0].text),name=row[1].text)
                   elif row[2]==instance:
                       
                       db.update_products('products.db', int(row[0].text),price=row[2].text.replace('Ugx ',''))
       
    def add_products(self):
        self.heading.clear_widgets()
        product_layout=GridLayout(cols =3,size_hint_y=None)
        product_layout.bind(minimum_height =product_layout.setter('height'))
        product_layout.add_widget(Label(text='',size_hint_x=0.2,font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100))
        product_layout.add_widget(Label(text='Please Add Products',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100,size_hint_x=0.6))
        product_layout.add_widget(Label(text='',size_hint_x=0.2,font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100))
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100,size_hint_x=0.2))
        product_name=TextInput (hint_text ='product name',size_hint_y=None, height=100, size_hint_x=0.6)
        product_layout.add_widget(product_name)
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100 ,size_hint_x=0.2))
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100,size_hint_x=0.2))
        min_qty=TextInput (hint_text ='minimum quantity',size_hint_y=None, height=100, size_hint_x=0.6,input_filter='int')
        product_layout.add_widget(min_qty)
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100 ,size_hint_x=0.2))
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100 ,size_hint_x=0.2))
        
        product_price =TextInput(hint_text ='product price',size_hint_y=None, height=100,input_filter='int')
        product_layout.add_widget(product_price)
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100 ,size_hint_x=0.2))
        
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=100 ,size_hint_x=0.2))
        product_layout.add_widget(Button(text ='submit' ,size_hint_y=None, height=100 ,on_press=lambda instance:self.submit_products_data(instance, product_name, product_price, min_qty),size_hint_x=0.6))
        self.sales_layout.add_widget(product_layout)
        product_layout.add_widget(Label(text='',font_size=35,bold=True, color=(0,0,1,1),size_hint_y=None, height=70 ,size_hint_x=0.2))
        
        
    def submit_products_data(self,instance, name,price,min_qty):
        if name.text !='' and price.text!='':
            db=Database(['products.db'])
            id=db.get_product_id('products.db',name.text)
            if not id:
                db.add_products('products.db',name.text,int(price.text), int(min_qty.text))
                price.text=''
                name.text=''
                min_qty.text=''
            else:
                pop_msg('error',f'{name.text} already exists please verify before adding duplicate records')
            
           
    def products_data(self, instance):
        
        self.heading.clear_widgets()
        self.sales_layout.clear_widgets()
        head=GridLayout(cols =3,size_hint_y=None, height=70)
        self.heading.add_widget(head)
        head.add_widget(Label(text ='product id', size_hint_x=0.2,bold=True, font_size=30,color=(0,0,0,1)))
        head.add_widget(Label(text ='product name', size_hint_x=0.5, bold=True, font_size=30,color=(0,0,0,1)))
        
        head.add_widget(Label(text ='price',size_hint_x=0.3, font_size=30,bold=True, color=(0,0,0,1)))
        self.data_block=GridLayout(cols =4,size_hint_y=None)
        self.data_block.bind(minimum_height =self.data_block.setter('height'))
        db=Database(['products.db'])
        for row in db.get_products('products.db'):
            product_id =TextInput(size_hint_y =None, height =70,readonly =True, text=str(row[0]) ,size_hint_x=0.1)
            self.data_block.add_widget(product_id)
            product_name =TextInput(size_hint_y =None, height =70,text=row[1], size_hint_x=0.35)
            self.data_block.add_widget(product_name)
            min_qty =TextInput(size_hint_y =None, height =70,text=str(row[3]), size_hint_x=0.15,input_filter='int',multiline=False)
            self.data_block.add_widget(min_qty)
            min_qty.bind(focus =self.keyboard_height)
            min_qty.bind(text =self.update_products)
            product_name.bind(text=self.update_products)
            product_name.bind(focus =self.keyboard_height)
            product_price=TextInput(text =f'Ugx {str(row[2])}',size_hint_y=None, height=70,size_hint_x=0.3,input_filter='int',multiline=False)
            product_price.bind(focus =lambda instance,value:(self.keyboard_height(instance, value),self.price_on_focus(instance, value))) 
            product_price.bind(text =self.update_products)
            self.data_block.add_widget(product_price)
            
            self.product_rows.append((product_id, product_name, product_price))
        self.sales_layout.add_widget(self.data_block)
       
 
class MyApp(MDApp):
    def build(self):
      #  return IncomeAndExpenses(1).call_income(income =True)
        return Welcome()

if __name__ == '__main__':
    MyApp().run()