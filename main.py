#!/usr/bin/env python
# coding: utf-8

# In[25]:


from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
import time
import json
import sys
import os

# Theme
from jupyterthemes import jtplot
jtplot.style(theme='chesterish', context='notebook', ticks=True, grid=False)

# User libraries
from Token import *
from factions import *
from players import *
from nfts import *


# ### Faction configuration
# - Faction 0 = MUD
# - Faction 1 = ONI
# - Faction 2 = USTUR

# In[26]:


FACTIONS = [
    'MUD',
    'ONI',
    'USTUR',
]
# MUD = 0
# ONI = 1
# USTUR = 2
LOAD_FROM_FILES = False


# #### General DataFrames

# In[27]:


FACTIONS_INVENTORY_DF = pd.DataFrame()


# #### Functions

# In[28]:


# Wallet balance getter
client = Client("https://api.mainnet-beta.solana.com")
def get_balance(wallet):
    tokens = client.get_token_accounts_by_owner(
        wallet, 
        TokenAccountOpts(program_id='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', encoding='jsonParsed')
    )
    return tokens_from_dict(tokens)

# Get players balances
def get_players_balances(player_list):
    data = []
    for i, player in enumerate(player_list):
        try:
            results = get_balance(player.public_key)
            atlas = 0
            polis = 0
            for value in results.result.value:
                if 'atlas' in value.account.data.parsed.info.mint.lower(): 
                    atlas = value.account.data.parsed.info.token_amount.ui_amount
                if 'polis' in value.account.data.parsed.info.mint.lower(): 
                    polis = value.account.data.parsed.info.token_amount.ui_amount
            print(f"Current wallet: {player.public_key}, {i+1} of {len(player_list)}; Balance: A {atlas}, P {polis}")
            data_to_append = {
                    'Faction' : FACTIONS[player.faction],
                    'Wallet': player.public_key,
                    "Atlas": atlas,
                    "Polis":polis,
                    "NFTS": player.balances,
                    "NFT_sum_usdc": player.balance,
                }
            data.append(data_to_append)
        except:
            print(f"Error in {i+1} of {len(player_list)}")
        time.sleep(2)
    return pd.DataFrame(data=data)

# convert str back to a class
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


# ### Create dataframe (if not exists csv)

# In[29]:


if not os.path.exists('./leaderboard-data.csv'):
    data = {
        'Faction' : [float('NaN')],
        'Wallet': [float('NaN')],
        "Atlas": [float('NaN')],
        "Polis": [float('NaN')],
        "NFTS": [float('NaN')],
        "NFT_sum_usdc": [float('NaN')],
    }
    DF = pd.DataFrame(data=data)
else:
    DF = pd.read_csv('./leaderboard-data.csv', index_col=False)
DF.head()


# In[30]:


player_amount = 600
player_amount_already_collected = 0
player_per_page = 50
players_list = []
if not LOAD_FROM_FILES:
    # requests
    for i in range(int(player_amount_already_collected / player_per_page), int( player_amount / player_per_page)):
        players_request = requests.get(f"https://galaxy.staratlas.com/leaderboards/players/?page={i}")
        # Get player list
        obj = players_from_dict(json.loads(players_request.text))
        players_list += obj
    Players_DataFrame = pd.DataFrame(players_list)
    Players_DataFrame.to_csv('./players.csv', index=False)
    print(len(players_list))


# In[31]:


# request
factions_request = requests.get("https://galaxy.staratlas.com/leaderboards/factions")
# Get faction list
factions_list = factions_from_dict(json.loads(factions_request.text))


# In[32]:


# GET nfts list
nfts_request = requests.get('https://galaxy.staratlas.com/nfts')
nfts_list = nfts_from_dict(json.loads(nfts_request.text))


# In[33]:


NFTS_DF = pd.DataFrame(nfts_list)
NFTS_DF[['name', 'mint']]


# In[34]:


if LOAD_FROM_FILES:
    players_balances = pd.read_csv('./Playerbalances.csv')
else:
    print('Starting data download')
    # Get players balances
    players_balances = get_players_balances(players_list)
players_balances.head()


# In[45]:


# merge results with total DF
# merge only if wallet not existis
players_balances_bkp = players_balances
players_balances_bkp.to_csv('./Playerbalances.csv', index=False)
columns = list(DF.columns) # get DF columns
DF = DF.loc[players_balances.Wallet.isin(DF.Wallet)] = players_balances[columns] # update old values
# remove values alreary in DF
# players_balances.drop(index=players_balances.Wallet.isin(DF.Wallet).index) 
DF = DF.append(players_balances, ignore_index=True) # append new values
DF = DF.drop_duplicates(subset=['Wallet']) # remove duplicates
# DF.head()
# Save DF
DF.to_csv('./leaderboard-data.csv', index=False)
DF.head()


# In[35]:


FACTIONS_INVENTORY_DF['faction name'] = 'MUD'
FACTIONS_INVENTORY_DF[NFTS_DF['name']] = '-'
FACTIONS_INVENTORY_DF.loc[0] = [i for i in range(NFTS_DF['name'].size)]
FACTIONS_INVENTORY_DF.loc[1] = [i for i in range(NFTS_DF['name'].size)]
FACTIONS_INVENTORY_DF.loc[2] = [i for i in range(NFTS_DF['name'].size)]
FACTIONS_INVENTORY_DF.head()


# #### NFT Separation (Type and amount)

# In[36]:


mud_nfts = players_balances.loc[players_balances['Faction'] == 'ONI']
mud_nfts.loc[mud_nfts['Wallet'] == 'G3YpYsexKbYNCbVdufR2LMcc6v12zPLtHAk51yG9GcEv']


# In[39]:


# MUD
mud_nfts = players_balances.loc[players_balances['Faction'] == 'MUD']['NFTS']
FACTIONS_INVENTORY_DF.at[0,'faction name'] = 'MUD'
for mud in mud_nfts:
    for value in eval(str(mud)):
         FACTIONS_INVENTORY_DF.at[0, NFTS_DF.loc[NFTS_DF['mint']== value.mint]['name'].values[0]] += value.quantity
# ONI
oni_nfts = players_balances.loc[players_balances['Faction'] == 'ONI']['NFTS']
FACTIONS_INVENTORY_DF.at[1,'faction name'] = 'ONI'
for oni in oni_nfts:
    for value in eval(str(oni)):
         FACTIONS_INVENTORY_DF.at[1, NFTS_DF.loc[NFTS_DF['mint']== value.mint]['name'].values[0]] += value.quantity
# USTUR
ustur_nfts = players_balances.loc[players_balances['Faction'] == 'USTUR']['NFTS']
FACTIONS_INVENTORY_DF.at[2,'faction name'] = 'USTUR'
for ustur in ustur_nfts:
    for value in eval(str(oni)):
         FACTIONS_INVENTORY_DF.at[2, NFTS_DF.loc[NFTS_DF['mint']== value.mint]['name'].values[0]] += value.quantity
FACTIONS_INVENTORY_DF.to_csv('./faction_inventory.csv', index=False)
FACTIONS_INVENTORY_DF.head()


# In[40]:


group = FACTIONS_INVENTORY_DF[['faction name','Pearce F4','Ogrika Thripid','VZUS opod','Calico Guardian']]
group.plot(kind='bar', x='faction name')
plt.title(f'Ships per faction (top {players_balances["Faction"].size}) leaderboard')
plt.savefig('./faction_ships.jpg')


# In[46]:


DF.groupby('Faction').sum()


# In[47]:


DF.sort_values(by=['Polis','Atlas'])


# In[65]:


# count of each faction
g = DF.groupby('Faction').count()
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.pie(
    g['Wallet'],
    explode=explode,
    labels=g.index,
    autopct='%1.1f%%',
    shadow=True,
    startangle=90
)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title(f'Players per faction (top {DF["Faction"].size} leaderboard)')
plt.savefig('./players_p_faction_leaderboard.jpg')
g.head()


# In[49]:


sns.displot(
    data=DF,
    x="Polis", hue="Faction",
    kind="kde", height=6,
    multiple="fill", clip=(0, None),
    palette="ch:rot=-.25,hue=1,light=.75",
)
plt.savefig("polis_per_faction.jpg")


# In[50]:


# Separate by Faction
MUD = DF.loc[DF['Faction'] == 'MUD']
ONI = DF.loc[DF['Faction'] == 'ONI']
USTUR = DF.loc[DF['Faction'] == 'USTUR']
sns.pairplot(DF, hue="Faction", )
plt.savefig('./pairplot_faction.jpg')


# In[66]:


f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5), sharex=False)

# Generate some sequential data
gp = DF.sort_values(by=['Atlas', 'Polis'])
gp = gp.groupby('Faction').sum()
x = gp.index
y1 = gp['Polis']
sns.barplot(x=x, y=y1, palette="rocket", ax=ax1)
ax1.axhline(0, color="k", clip_on=False)
ax1.set_ylabel("Polis")

# Center the data to make it diverging
y2 = gp['Atlas']
sns.barplot(x=x, y=y2, palette="rocket", ax=ax2)
ax2.axhline(0, color="k", clip_on=False)
ax2.set_ylabel("Atlas")

# Randomly reorder the data to make it qualitative
y3 = gp['NFT_sum_usdc']
sns.barplot(x=x, y=y3, palette="rocket", ax=ax3)
ax3.axhline(0, color="k", clip_on=False)
ax3.set_ylabel("NFT Balance")

# Finalize the plot
sns.despine(bottom=True)
plt.title(f"Total Tokens distribution Top {DF['Faction'].size} Leaderboard")
plt.setp(f.axes, yticks=[])
plt.tight_layout(h_pad=2)
plt.savefig('./balance_per_faction.jpg')


# In[56]:


DF_Factions = pd.DataFrame(factions_list)
DF_Factions['faction'].replace({0:'MUD',1:'ONI',2:'USTUR'}, inplace=True)

explode = (0, 0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.pie(
    DF_Factions['total_players'],
    explode=explode,
    labels=DF_Factions['faction'],
    autopct='%1.1f%%',
    shadow=True,
    startangle=90
)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Players per faction')
DF_Factions['balance'] = [row['total'] for row in DF_Factions['value']]

ax2.pie(
    DF_Factions['balance'],
    explode=explode,
    labels=DF_Factions['faction'],
    autopct='%1.1f%%',
    shadow=True,
    startangle=90
)
ax2.set_title('Economy (NFT Balance)')
ax2.axis('equal') 

plt.savefig('./faction_share.jpg')
plt.show()


# In[53]:


ax = sns.countplot(data=DF, x='Faction')
ax.set_title(f'Wallets per faction on top {DF["Faction"].size} leaderboard')
ax.set_ylabel('Amount')
plt.savefig('./wallets_per_faction.jpg')


# In[54]:


DF.groupby('Faction').mean().plot(kind='bar')
plt.title('Average purchasing power per faction')
plt.savefig('./average_purchasing_power.jpg')


# In[67]:


f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5), sharex=False)

# Generate some sequential data
gp = DF.sort_values(by=['Atlas', 'Polis'])
gp = gp.groupby('Faction').mean()
x = gp.index
y1 = gp['Polis']
sns.barplot(x=x, y=y1, ax=ax1)
ax1.axhline(0, color="k", clip_on=False)
ax1.set_ylabel("Polis")

# Center the data to make it diverging
y2 = gp['Atlas']
sns.barplot(x=x, y=y2, ax=ax2)
ax2.axhline(0, color="k", clip_on=False)
ax2.set_ylabel("Atlas")

# Randomly reorder the data to make it qualitative
y3 = gp['NFT_sum_usdc']
sns.barplot(x=x, y=y3, ax=ax3)
ax3.axhline(0, color="k", clip_on=False)
ax3.set_ylabel("NFT Balance")

# Finalize the plot
sns.despine(bottom=True)
plt.title(f"Average purchasing power per faction detailed")
plt.setp(f.axes, yticks=[])
plt.tight_layout(h_pad=2)
plt.savefig('./average_purchasing_power_details.jpg')

