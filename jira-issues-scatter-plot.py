
import pandas as pd
import numpy as np
import datetime
import random
from dateutil.parser import parse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

class Quadrant():
    positions = []

    def getPosition(self, quadrant):

        try:
            region = str(quadrant).split("-")
            business = region[0]
            technical = region[1]

            flag = False

            while not flag:
                x = random.randrange(self.regionValue(technical), self.regionValue(technical) + 9, 2)
                y = random.randrange(self.regionValue(business), self.regionValue(business) + 9, 2)

                position = str(x) + "-" + str(y)
                if position not in self.positions:
                    flag = True
                    self.positions.append(position)

            x = float(x) + random.uniform(-0.5, 0.5)
            y = float(y) + random.uniform(-0.5, 0.5)

            return str(x) + "-" + str(y)
            # return position
        except:
            return 0

    def regionValue(self, region):
        if region == 'high':
            return 21
        elif region == 'medium':
            return 11
        elif region == 'low':
            return 1


def getAge(value):
    now = datetime.datetime.now()
    td = now - parse(value)
    return td.days
    


def initQuadrants():
    quadrants = {}
    level = ["medium", "high", "low"]
    for l in level:
        for l2 in level:
            pass

    return quadrants


def getPosition(value):
    return quadrant.getPosition(value)


def convertIssueType(tp):
    if tp == "Epic":
        return 100
    else:
        return 30

# load jira export
df = pd.read_csv('viudaten.csv')

# Remove not needed columns
columns = ["Issue id", "Assignee", "Reporter", "Priority", "Status", "Component/s", "Custom field (PrestaShop Entity)", "Custom field (PrestaShop Entity).1", "Custom field (PrestaShop Entity).2"]
for column in columns:
    df.drop(column, 1, inplace=True);



df["Quadrant"] = df["Custom field (Business Value)"] + "-" + df["Custom field (Technical Complexity)"]

df["Age"] = df["Created"].apply(getAge);

quadrants = initQuadrants()



global quadrant
quadrant = Quadrant()



df["Position"] = df["Quadrant"].apply(getPosition)

pos = df["Position"].str.split("-",1,True)
pos.rename(columns={0:'X', 1:'Y'}, inplace=True)

df = df.join(pos)



    
df["IssueTypeValue"] = df["Issue Type"].apply(convertIssueType)


# In[95]:



plt.close('all')
plt.style.use('ggplot')
fig = plt.figure(figsize=(15,15))
fig = ax = fig.add_subplot(111)


df2 = df[df.Position != 0]

plt.scatter(df2.X, df2.Y, s=df.IssueTypeValue)


  
def annotate_df(row):  
    plt.annotate(row["Issue key"] + " (" + str(row["Age"]) + ")", xy=(row["X"], row["Y"]),
                xytext=(-15,-20), 
                textcoords='offset points',
                size=8, 
                color='darkslategrey')

df2.apply(annotate_df, axis=1)

rectangles = {'' : mpatch.Rectangle((0,10), 10, 10, alpha=0.2, facecolor="#1fe700"),
              'To Do' : mpatch.Rectangle((0,20), 30, 10, alpha=0.2, facecolor="#1fe700"),
              'Dont\'s' : mpatch.Rectangle((0,0), 30, 10, alpha=0.2, facecolor="#ff0000"),
              ' ' : mpatch.Rectangle((10,10), 20, 10, alpha=0.2, facecolor="#ff0000")}

for r in rectangles:
    fig.add_artist(rectangles[r])
    rx, ry = rectangles[r].get_xy()
    cx = rx + rectangles[r].get_width()/2.0
    cy = ry + rectangles[r].get_height()/2.0

    ax.annotate(r, (cx, cy), color='w', weight='bold', 
                fontsize=20, ha='center', va='center')
    
fig.set_xlim((0, 30))
fig.set_ylim((0, 30))
fig.set_aspect('equal')

plt.savefig('scatter.png', dpi=200)

#sc.get_figure()
#fig.savefig("figure.pdf", dpi=300)


df2 = df[df.Position != 0]

df2[['Position', 'X','Y','Issue key']]
