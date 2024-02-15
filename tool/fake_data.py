from faker import Faker
import random
import re

# 创建一个Faker实例
fake = Faker()

# 定义一些职位名称和公司类型的列表

company_types = [
    'Tech',
    'Marketing',
    'Agency',
    'Studio',
    'Co.',
    'Estate',
]

job_titles = [
    'Software Engineer', 
    'Pharmaceutical Sales Representative', 
    'Management Consultant', 
    'Marketing Director', 
    'Production Manager', 
    'Financial Analyst', 
    'Retail Store Manager', 
    'Teacher', 
    'Nurse Practitioner', 
    'Hotel Manager', 
    'Data Scientist', 
    'Lab Technician', 
    'HR Specialist', 
    'SEO Specialist', 
    'Quality Assurance Engineer', 
    'Accountant', 
    'Sales Associate', 
    'Principal', 
    'Physical Therapist', 
    'Chef', 
    'Machine Learning Engineer', 
    'Clinical Research Associate', 
    'Business Analyst', 
    'Brand Manager', 
    'Operations Manager', 
    'Investment Banker', 
    'Merchandiser', 
    'Curriculum Developer', 
    'Registered Nurse', 
    'Event Coordinator', 
    'Network Engineer', 
    'Pharmacy Manager', 
    'Recruitment Consultant', 
    'Content Strategist', 
    'Supply Chain Analyst', 
    'Risk Manager', 
    'Cashier', 
    'Special Education Teacher', 
    'Dietitian', 
    'Front Desk Agent', 
    'Cybersecurity Specialist', 
    'Medical Science Liaison', 
    'Talent Acquisition Manager', 
    'Public Relations Manager', 
    'Logistics Coordinator', 
    'Compliance Officer', 
    'Visual Merchandiser', 
    'Instructional Designer', 
    'Occupational Therapist', 
    'Travel Agent'
]

def generate_phone_number():
    # 定义电话号码格式，例如 '(###) ###-####' 的美国格式
    formats = ['(###) ###-####', '###-###-####', '+1-###-###-####']
    # 随机选择一个格式
    phone_format = random.choice(formats)
    # 生成电话号码
    phone_number = fake.numerify(text=phone_format)
    return phone_number

# 定义生成数据的数量
num_data = 100000

# 打开一个文件来写入生成的数据
with open('ner_training_data.txt', 'w', encoding='utf-8') as file:
    for _ in range(num_data):
        
        type_num = random.randint(0,5)
        # 将数据写入文件，并添加标签
        if type_num == 0:
            name = fake.name()
            file.write(f"{name}=PERSON\n")
            # file.write("\n")
        elif type_num == 1:
            while True:
                address = fake.address().split('\n')
                if not re.search(r'estate', address[0], re.IGNORECASE):
                    file.write(f"{address[0]}=ADDRESS\n")
                    break
            # file.write("\n")
        elif type_num == 2:
            company = f"{fake.company()} {random.choice(list(company_types))}"
            file.write(f"{company}=ORG\n")
            # file.write("\n")
        elif type_num == 3:
            job_title = random.choice(list(job_titles))
            file.write(f"{job_title}=POSITION\n")
            # file.write("\n")
        # elif type_num == 4:
        #     url = fake.url()
        #     file.write(f"{url}=URL\n")
        #     # file.write("\n")
        # elif type_num == 5:
        #     email = fake.email()
        #     file.write(f"{email}=EMAIL\n")
            # file.write("\n")
        elif type_num == 4:
            phone = generate_phone_number()
            file.write(f"{phone}=PHONE\n")
            # file.write("\n")
        else:
            while True:
                address = fake.address().split('\n')
                if not re.search(r'estate', address[1], re.IGNORECASE):
                    file.write(f"{address[1]}=ADDRESS\n")
                    break
            # file.write("\n")


        

print("Data generation complete.")
