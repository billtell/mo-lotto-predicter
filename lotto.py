
# data source:https://www.molottery.com/numbers/winning_nums.jsp#Lotto

#Project Overview:

   #*Obtain Historic Lottery Data

    #*Format Data in Dataframe

    #*Analyze / Visualize

    #*Make Predictions based on different assumptions
      

# # import and organize data into dataframe

import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.pyplot import figure
import random
    
df = pd.read_excel (r'lotto.xlsx', names= ['Draw Date',
                    'NumbersAsDrawn','NumbersInOrder','Jackpot','6of6','5of6',
                    '4of6','3of6']) 
print (df)

new_df = df.drop(columns=['NumbersAsDrawn','Jackpot','6of6','5of6','4of6','3of6'], axis=1)


new_df[['Ball1','Ball2','Ball3','Ball4','Ball5','Ball6']]= new_df['NumbersInOrder'].str.split('--', expand=True)
new_df.drop(0, inplace=True)

new_df


new_df.Ball1 = new_df.Ball1.astype('int')
new_df.Ball2 = new_df.Ball2.astype('int')
new_df.Ball3 = new_df.Ball3.astype('int')
new_df.Ball4 = new_df.Ball4.astype('int')
new_df.Ball5 = new_df.Ball5.astype('int')
new_df.Ball6 = new_df.Ball6.astype('int')


new_df.info()


# ## Analyze and Visualize Data 

#set figure parameters
plt.rcParams['figure.figsize'] = [12.0, 8.0]
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 100

plt.rcParams['font.size'] = 12
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['figure.titlesize'] = 'medium'

#statistical overview
new_df.describe()

ax = sns.countplot(x="Ball1", data=new_df)
plt.xlabel('Numbers Drawn')
plt.ylabel('Count')
plt.title('Ball 1 Distribution')


ax = sns.countplot(x="Ball2", data=new_df)
plt.xlabel('Numbers Drawn')
plt.ylabel('Count')
plt.title('Ball 2 Distribution')
#specify positions of ticks on x-axis and y-axis
for ax, label in enumerate(ax.get_xticklabels()):
    if ax % 5 == 0:  # every 5th label is kept
        label.set_visible(True)
    else:
        label.set_visible(False)


ax = sns.countplot(x="Ball3", data=new_df)
plt.xlabel('Numbers Drawn')
plt.ylabel('Count')
plt.title('Ball 3 Distribution')
for ax, label in enumerate(ax.get_xticklabels()):
    if ax % 5 == 0:  # every 5th label is kept
        label.set_visible(True)
    else:
        label.set_visible(False)


ax = sns.countplot(x="Ball4", data=new_df)
plt.xlabel('Numbers Drawn')
plt.ylabel('Count')
plt.title('Ball 4 Distribution')
for ax, label in enumerate(ax.get_xticklabels()):
    if ax % 5 == 0:  # every 5th label is kept
        label.set_visible(True)
    else:
        label.set_visible(False)

ax = sns.countplot(x="Ball5", data=new_df)
plt.xlabel('Numbers Drawn')
plt.ylabel('Count')
plt.title('Ball 5 Distribution')


ax = sns.countplot(x="Ball6", data=new_df)
plt.xlabel('Numbers Drawn')
plt.ylabel('Count')
plt.title('Ball6 Distribution')


# # Aggregate Ball1-Ball5 into a Total column

col_list= list(new_df.columns)
col_list.remove('Draw Date')
col_list.remove('NumbersInOrder')
new_df['Total'] = new_df[col_list].sum(axis=1)
new_df


ax = sns.countplot(x="Total", data=new_df)
plt.xlabel('Sum Total of Balls 1 - 6')
plt.ylabel('Count')
plt.title('Sum Total Distribution')
plt.xticks(rotation=90)
for ax, label in enumerate(ax.get_xticklabels()):
    if ax % 3 == 0:  # every @nd label is kept
        label.set_visible(True)
    else:
        label.set_visible(False)

new_df.describe()


#for total: 68%, 1 std, of all totals are equal to approx 105 - 165
#for total: 95%, 2 std, of all totals are equal to approx  75 - 195

#cases around the mean
new_df.query('Total>130 & Total<140').head(15)


# # examine spacing between numbers
diff_df = pd.DataFrame()

diff_df['Draw Date'] = new_df['Draw Date']
diff_df['b2-b1'] = new_df['Ball2'] - new_df['Ball1']
diff_df['b3-b2'] = new_df['Ball3'] - new_df['Ball2']
diff_df['b4-b3'] = new_df['Ball4'] - new_df['Ball3']
diff_df['b5-b4'] = new_df['Ball5'] - new_df['Ball4']
diff_df['b6-b5'] = new_df['Ball6'] - new_df['Ball5']
diff_df['b6-b1'] = new_df['Ball6'] - new_df['Ball1']
diff_df

diff_df.describe()

ax = sns.countplot(x="b2-b1", data=diff_df)
plt.xlabel('B2-B1 Difference')
plt.ylabel('Count')
plt.title('Ball2 - Ball1')

ax = sns.countplot(x="b3-b2", data=diff_df)
plt.xlabel('B3-B2 Difference')
plt.ylabel('Count')
plt.title('Ball3 - Ball2')


ax = sns.countplot(x="b4-b3", data=diff_df)
plt.xlabel('B4-B3 Difference')
plt.ylabel('Count')
plt.title('Ball4 - Ball3')


ax = sns.countplot(x="b5-b4", data=diff_df)
plt.xlabel('B5-B4 Difference')
plt.ylabel('Count')
plt.title('Ball5 - Ball4')


ax = sns.countplot(x="b6-b5", data=diff_df)
plt.xlabel('B6-B5 Difference')
plt.ylabel('Count')
plt.title('Ball6 - Ball5')


ax = sns.countplot(x="b6-b1", data=diff_df)
plt.xlabel('B6-B1 Difference')
plt.ylabel('Count')
plt.title('Total Difference')


# # Make predictions:

# # Approach 1: sort out recent numbers


recent=new_df.head(14)
recent

ln=sns.lineplot(data=recent, x="Draw Date", y="Total")
plt.xticks(rotation=90)


#what has been happening lately
#will means return to "natural position"?
recent.describe()


#use a for loop to sort out recent numbers 
# recent is last 2 weeks
#try 2 approaches : put all into 1 set or keep in separate groups

ball1_recent=list(set(recent.Ball1))
ball2_recent=list(set(recent.Ball2))
ball3_recent=list(set(recent.Ball3))
ball4_recent=list(set(recent.Ball4))
ball5_recent=list(set(recent.Ball5))
ball6_recent=list(set(recent.Ball6))

picks_v1=[]

for ball1_picks in range(1, 13):
    if ball1_picks in ball1_recent:
        picks_v1.append(ball1_picks)
for ball2_picks in range(2, 28):
    if ball2_picks in ball2_recent:
        picks_v1.append(ball2_picks)
for ball3_picks in range(3, 39):
    if ball3_picks in ball3_recent:
        picks_v1.append(ball3_picks)   
for ball4_picks in range(4, 43):
    if ball4_picks in ball4_recent:
        picks_v1.append(ball4_picks)       
for ball5_picks in range(10, 44):
    if ball5_picks in ball5_recent:
        picks_v1.append(ball5_picks)
for ball6_picks in range(14, 45):
    if ball6_picks in ball6_recent:
        picks_v1.append(ball6_picks)
print(picks_v1)


picks_v1 = list(set(picks_v1))
print(picks_v1, end = ' ')

len(picks_v1)

ball1_recent=list(set(recent.Ball1))
ball2_recent=list(set(recent.Ball2))
ball3_recent=list(set(recent.Ball3))
ball4_recent=list(set(recent.Ball4))
ball5_recent=list(set(recent.Ball5))

picks_b1=[]
picks_b2=[]
picks_b3=[]
picks_b4=[]
picks_b5=[]
picks_b6=[]

for ball1_picks in range(1, 20):
    if ball1_picks in ball1_recent:
        picks_b1.append(ball1_picks)
for ball2_picks in range(2, 30):
    if ball2_picks in ball2_recent:
        picks_b2.append(ball2_picks)
for ball3_picks in range(3, 35):
    if ball3_picks in ball3_recent:
        picks_b3.append(ball3_picks)
for ball4_picks in range(4, 43):
    if ball4_picks in ball4_recent:
        picks_b4.append(ball4_picks)
for ball5_picks in range(10, 44):
    if ball5_picks in ball5_recent:
        picks_b5.append(ball5_picks)
for ball6_picks in range(14, 45):
    if ball6_picks in ball5_recent:
        picks_b6.append(ball6_picks)
        
picks_total=list(picks_b1),list(picks_b2),list(picks_b3),list(picks_b4),list(picks_b5),list(picks_b6)


print(picks_b1)


print(picks_total)


import random


#recents sorted out

a=(random.sample(picks_b1, k=1))
while True:
    a1=(random.sample(picks_b2, k=1))
    if a1>a:
        break
while True:
    a2=(random.sample(picks_b3, k=1))
    if a2>a1:
        break
while True:
    a3=(random.sample(picks_b4, k=1))
    if a3>a2:
        break
while True:
    a4=(random.sample(picks_b5, k=1))
    if a4>a3:
        break
while True:
    a5=(random.sample(picks_b6, k=1))
    if a5>a4:
        break
print("Random Selection variation 1:", a, a1, a2, a3, a4, a5)
a_all = a+a1+a2+a3+a4+a5
print("Sum of Selection:", sum(a_all))


sample_size = 6
rand_select = [picks_v1[i] for i in sorted(random.sample(range(len(picks_v1)), sample_size))]
print("Random Selection w/o recents:", rand_select)
print("Sum of Selection:", sum(rand_select))


random_picks=sorted(random.sample(range(1,45), k=6)) 
print("Random Selection: ",random_picks)
print("Sum of Selection:", sum(random_picks))


# # Approach 2: Index Position Sort

#instead of trying to sort out the recently drawn numbers, 
#look for the ones that haven't been drawn in the longest time.
#in other words, sort by index position
#this is an extension of assumption 1:  numbers will not quickly repeat


Ball1=list(new_df.Ball1)
Ball2=list(new_df.Ball2)
Ball3=list(new_df.Ball3)
Ball4=list(new_df.Ball4)
Ball5=list(new_df.Ball5)
Ball6=list(new_df.Ball6)

key=(range(1,21))
ball1_sort=[]
for i in range (1,21):
    position = Ball1.index(i)+1
    ball1_sort.append(position)
ball1_dict=dict(zip(key, ball1_sort))


b1_picks=[]
for value in sorted(ball1_dict.values()):
    for key in ball1_dict.keys():
        if ball1_dict[key] == value:
            b1_picks.append(key)
            print(key, value)


key=(range(2,31))
ball2_sort=[]
for i in range (2,31):
    position = Ball2.index(i)+1
    ball2_sort.append(position)
ball2_dict=dict(zip(key, ball2_sort))


b2_picks=[]
for value in sorted(ball2_dict.values()):
    for key in ball2_dict.keys():
        if ball2_dict[key] == value:
            b2_picks.append(key)
            print(key, value)


key=(range(3,36))
ball3_sort=[]
for i in range (3,36):
    position = Ball3.index(i)+1
    ball3_sort.append(position)
ball3_dict=dict(zip(key, ball3_sort))


b3_picks=[]
for value in sorted(ball3_dict.values()):
    for key in ball3_dict.keys():
        if ball3_dict[key] == value:
            b3_picks.append(key)
            print(key, value)


key=(range(6,41))
ball4_sort=[]
for i in range (6,41):
        position = Ball4.index(i)+1
        ball4_sort.append(position) 
ball4_dict=dict(zip(key, ball4_sort))
ball4_dict

b4_picks=[]
for value in sorted(ball4_dict.values()):
    for key in ball4_dict.keys():
        if ball4_dict[key] == value:
            b4_picks.append(key)
            print(key, value)

key=(range(11,44))
ball5_sort=[]
for i in range (11,44):
        position = Ball5.index(i)+1
        ball5_sort.append(position) 
ball5_dict=dict(zip(key, ball5_sort))
ball5_dict


b5_picks=[]
for value in sorted(ball5_dict.values()):
    for key in ball5_dict.keys():
        if ball5_dict[key] == value:
            b5_picks.append(key)
            print(key, value)

key=(range(18,45))
ball6_sort=[]
for i in range (18,45):
        position = Ball6.index(i)+1
        ball6_sort.append(position) 
ball6_dict=dict(zip(key, ball6_sort))
ball6_dict

b6_picks=[]
for value in sorted(ball6_dict.values()):
    for key in ball6_dict.keys():
        if ball6_dict[key] == value:
            b6_picks.append(key)
            print(key, value)

b1_all=b1_picks[:]
print(b1_all)

b1_picks_recent=b1_picks[:5]
print(b1_picks_recent)

b1_picks_oldest=b1_picks[-5:]
print(b1_picks_oldest)


#slice by index position
b1_picks_recent=b1_picks[:8]
b1_picks_middle=b1_picks[6:17]
b1_picks_oldest=b1_picks[-3:]
b1_picks_all=b1_picks[:]

b2_picks_recent=b2_picks[:14]
b2_picks_middle=b2_picks[12:23]
b2_picks_oldest=b2_picks[-6:]
b2_picks_all=b2_picks[:]

b3_picks_recent=b3_picks[:15]
b3_picks_middle=b3_picks[13:31]
b3_picks_oldest=b3_picks[-3:]
b3_picks_all=b3_picks[:]

b4_picks_recent=b4_picks[:12]
b4_picks_middle=b4_picks[10:26]
b4_picks_oldest=b4_picks[-9:]
b4_picks_all=b4_picks[:]

b5_picks_recent=b5_picks[:17]
b5_picks_middle=b5_picks[15:29]
b5_picks_oldest=b5_picks[-5:]
b5_picks_all=b5_picks[:]

b6_picks_recent=b6_picks[:11]
b6_picks_middle=b6_picks[9:22]
b6_picks_oldest=b6_picks[-6:] # don't use these
b6_picks_all=b6_picks[:]


b1_picks_fresh=b1_picks[:8]
b1_picks_ripe=b1_picks[8:]

b2_picks_fresh=b2_picks[:13]
b2_picks_ripe=b2_picks[13:]

b3_picks_fresh=b3_picks[:16]
b3_picks_ripe=b3_picks[16:]

b4_picks_fresh=b4_picks[:13]
b4_picks_ripe=b4_picks[13:]

b5_picks_fresh=b5_picks[:17]
b5_picks_ripe=b5_picks[17:]

b6_picks_fresh=b6_picks[:11]
b6_picks_ripe=b6_picks[11:]


# #make predictions using the index position sort


#all middle index positions
x=(random.sample(b1_picks_recent, k=1))
while True:
    x1=(random.sample(b2_picks_recent, k=1))
    if x1>x:
        break
while True:
    x2=(random.sample(b3_picks_recent, k=1))
    if x2>x1:
        break
while True:
    x3=(random.sample(b4_picks_recent, k=1))
    if x3>x2:
        break
while True:
    x4=(random.sample(b5_picks_recent, k=1))
    if x4>x3:
        break
while True:
    x5=(random.sample(b6_picks_recent, k=1))
    if x5>x4:
        break
print("Random Selection variation 1:", x, x1, x2, x3, x4, x5)
x_all = x+x1+x2+x3+x4+x5
print("Sum of Selection:", sum(x_all))


#ball1 and ball5 recent
y=(random.sample(b1_picks_middle, k=1))
while True:
    y1=(random.sample(b2_picks_middle, k=1))
    if y1>y:
        break
while True:
    y2=(random.sample(b3_picks_middle, k=1))
    if y2>y1:
        break
while True:
    y3=(random.sample(b4_picks_recent, k=1))
    if y3>y2:
        break
while True:
    y4=(random.sample(b5_picks_recent, k=1))
    if y4>y3:
        break
while True:
    y5=(random.sample(b6_picks_recent, k=1))
    if y5>y4:
        break
print("Random Selection variation 2:", y, y1, y2, y3, y4, y5)
y_all = y+y1+y2+y3+y4+y5
print("Sum of Selection:", sum(y_all))


z=(random.sample(b1_picks_middle, k=1))
while True:
    z1=(random.sample(b2_picks_middle, k=1))
    if z1>z:
        break
while True:
    z2=(random.sample(b3_picks_middle, k=1))
    if z2>z1:
        break
while True:
    z3=(random.sample(b4_picks_middle, k=1))
    if z3>z2:
        break
while True:
    z4=(random.sample(b5_picks_middle, k=1))
    if z4>z3:
        break
while True:
    z5=(random.sample(b6_picks_recent, k=1))
    if z5>z4:
        break
print("Random Selection variation 3:", z, z1, z2, z3, z4, z5)
z_all = z+z1+z2+z3+z4+z5
print("Sum of Selection:", sum(z_all))


# # Approach 3: find combinations to target Sums within 1 std

mean_sort=new_df.query('Total>105 & Total<165')


#sns.countplot xrange: 105 - 165
ax = sns.countplot(x="Total", data=mean_sort)
plt.xlabel('Sum Total of Balls 1 - 6')
plt.ylabel('Count')
plt.title('Sum Total Distribution approx +/- 1 STD')
plt.xticks(rotation=90)
for ax, label in enumerate(ax.get_xticklabels()):
    if ax % 3 == 0:  # every @nd label is kept
        label.set_visible(True)
    else:
        label.set_visible(False)

#most popular sum
new_df.query('Total==125').head(15)

#plug&play query
new_df.query('Total==114')

# sort the Total index position
total_sum=list(new_df.Total)

total_sort=[]
for i in range (105,165):
    try:
        position = total_sum.index(i)+1
        total_sort.append(position)
        print(i, position)
    except ValueError:
        print(i, "Not in list")
        continue

key=(range(105,165))
total_sort=[]
for i in range (105,165):
    try:
        position = total_sum.index(i)+1
        total_sort.append(position)
        total_dict=dict(zip(key, total_sort))
    except ValueError:
        continue
        
total_picks=[]
for value in sorted(total_dict.values()):
    for key in total_dict.keys():
        if total_dict[key] == value:
            total_picks.append(key)
            print(key, value)


#reminder!
#for total: 68%, 1 std, of all totals are equal to approx 105 - 165
#for total: 95%, 2 std, of all totals are equal to approx 75 - 195

import itertools


# #create a function to target different sums with index position sort as the numeric input

# v1 = all numbers
# 
# v2 = middle indexed positions
# 
# v3 = b5 recent, b4-b2 are middile index position
# 
# v4 = oldest index positions

# In[ ]:


#targets: 115 , 157, 


#working from Ball6 down to Ball1 seemsed to work the best
def gen_combo_target_v1(s):
    for a in b6_picks_all:
        s2 = s - a
        for b in b5_picks_all:
            s3 = s2 - b
            for c in b4_picks_all:
                s4 = s3 - c
                for d in b3_picks_all:
                    s5 = s4 - d
                    for e in b2_picks_all:
                        s6 = s5 - e
                        yield ( s - a - b - c - d -e, e, d, c, b, a)


def gen_combo_target_v2(s):
    for a in b6_picks_middle:
        s2 = s - a
        for b in b5_picks_middle:
            s3 = s2 - b
            for c in b4_picks_middle:
                s4 = s3 - c
                for d in b3_picks_middle:
                    s5 = s4 - d
                    for e in b2_picks_middle:
                        s6 = s5 - e
                        yield ( s - a - b - c - d -e, e, d, c, b, a)

def gen_combo_target_v3(s):
    for a in b6_picks_recent:
        s2 = s - a
        for b in b5_picks_middle:
            s3 = s2 - b
            for c in b4_picks_middle:
                s4 = s3 - c
                for d in b3_picks_middle:
                    s5 = s4 - d
                    for e in b2_picks_middle:
                        s6 = s5 - e
                        yield ( s - a - b - c - d -e, e, d, c, b, a)


def gen_combo_target_v4(s):
    for a in b6_picks_all:
        s2 = s - a
        for b in b5_picks_all:
            s3 = s2 - b
            for c in b4_picks_all:
                s4 = s3 - c
                for d in b3_picks_oldest:
                    s5 = s4 - d
                    for e in b2_picks_all:
                        s6 = s5 - e
                        yield ( s - a - b - c - d -e, e, d, c, b, a)

combo_115=list(gen_combo_target_v2(115))
combo_115_df = pd.DataFrame (combo_115, columns = ['Ball1', 'Ball2', 'Ball3', 'Ball4', 'Ball5', 'Ball6'])
combo_115_df.query('Ball1<Ball2<Ball3<Ball4<Ball5<Ball6 & Ball1>0')


#explore
combo_115_df.query('Ball1==4 & Ball1<Ball2<Ball3<Ball4<Ball5<Ball6 & Ball1>0')


combo_115_df.query('Ball1==6 & Ball1<Ball2<Ball3<Ball4<Ball5<Ball6 & Ball1>0')


combo_115_df.query('Ball1==2 & Ball1<Ball2<Ball3<Ball4<Ball5<Ball6 & Ball1>0')


random.sample(total_picks, k=1)


#combo_--- = list(gen_combo_target_v2(---)) 
#combo_ ---= pd.DataFrame (combo_---, columns = ['Ball1', 'Ball2', 'Ball3', 'Ball4', 'Ball5'])
#combo_---.query('Ball1<Ball2<Ball3<Ball4<Ball5 & Ball1>0')

