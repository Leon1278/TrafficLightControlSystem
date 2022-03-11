import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Convert xml file into pandas df
# this code section should be used seperated before the rest of the script
"""df = pd.read_xml('tripinfo-15-iTLM-Q.xml')
print(df.head())
print("SAVING DATAFRAME...")
file_name = "df-tripinfo-15-iTLM-Q_mod"
df.to_csv(file_name, encoding='utf-8', index=False)"""

df = pd.read_csv('df-summary-1-default')
df12 = pd.read_csv('df-summary-125-default')
df11 = pd.read_csv('df-summary-15-default')
df01 = pd.read_csv('df-summary-25-default')

df02 = pd.read_csv('df-tripinfo-15-iTLM-Q_mod')
df03 = pd.read_csv('df-tripinfo-15-default')
df04 = pd.read_csv('df-tripinfo-15-InVehSt_mod')

df05 = pd.read_csv('df-statistics-1-default')
df06 = pd.read_csv('df-statistics-1-iTLM-Q')
df07 = pd.read_csv('df-statistics-1-InVehSt')

# line plot für die running vehicle
sns.lineplot(x='time', y='running', data=df, legend='brief')
sns.lineplot(x='time', y='running', data=df12, legend='brief')
sns.lineplot(x='time', y='running', data=df11, legend='brief')
sns.lineplot(x='time', y='running', data=df01, legend='brief')
plt.xlabel('Simulationsschritt')
plt.ylabel('Anzahl aktiver Fahrzeuge')
plt.legend(labels=['Skalierung 1', 'Skalierung 1.25', 'Skalierung 1.5', 'Skalierung 2.5'])

# line plot für die collisions (Summarys müssen erst in ein DataFrame konvertiert werden!)
sns.lineplot(x='time', y='collisions', data=df, legend='brief')
sns.lineplot(x='time', y='collisions', data=df01, legend='brief')
sns.lineplot(x='time', y='collisions', data=df01, legend='brief')

plt.xlabel('Simulation Step')
plt.ylabel('Collisions')
plt.legend(labels=['Default Scale 1', 'iTLM-Q Scale 1', 'InVehSt Scale 1'])

plt.tight_layout()
plt.savefig('', format="pdf")
plt.show()

# waiting time box plot
fig, axs = plt.subplots(3,1, sharex=True)
sns.boxplot(ax=axs[0], x='waitingTime', data=df03)
axs[0].set_title('Default')
axs[0].set_xlabel(None)
sns.boxplot(ax=axs[1], x='waitingTime', data=df02)
axs[1].set_title('iTLM-Q')
axs[1].set_xlabel(None)
sns.boxplot(ax=axs[2], x='waitingTime', data=df04)
axs[2].set_title('InVehSt')
axs[2].set_xlabel(None)
plt.xlabel('Wartezeit in Simulationsschritten')

plt.tight_layout()
plt.savefig('', format="pdf")
plt.show()

# duration violin plot
fig, axs = plt.subplots(3,1, sharex=True)
sns.violinplot(ax=axs[0], x='duration', data=df03)
axs[0].set_title('Default')
axs[0].set_xlabel(None)
sns.violinplot(ax=axs[1], x='duration', data=df02)
axs[1].set_title('iTLM-Q')
axs[1].set_xlabel(None)
sns.violinplot(ax=axs[2], x='duration', data=df04)
axs[2].set_title('InVehSt')
axs[2].set_xlabel(None)
plt.xlabel('Durchlaufzeit in (Simulations) Sekunden')

plt.tight_layout()
plt.savefig('', format="pdf")
plt.show()

# timeloss violin plot
fig, axs = plt.subplots(3,1, sharex=True)
sns.violinplot(ax=axs[0], x='timeLoss', data=df03)
axs[0].set_title('Default')
sns.violinplot(ax=axs[1], x='timeLoss', data=df02)
axs[1].set_title('iTLM-Q')
sns.violinplot(ax=axs[2], x='timeLoss', data=df04)
axs[2].set_title('InVehSt')

plt.tight_layout()
plt.savefig('', format="pdf")
plt.show()

# countPerPhaseDuration violin plot
fig, axs = plt.subplots(3,1, sharex=True)
sns.violinplot(ax=axs[0], x='countPerPhaseDuration', data=df05)
axs[0].set_title('Default')
axs[0].set_xlabel(None)
sns.violinplot(ax=axs[1], x='countPerPhaseDuration', data=df06)
axs[1].set_title('iTLM-Q')
axs[1].set_xlabel(None)
sns.violinplot(ax=axs[2], x='countPerPhaseDuration', data=df07)
axs[2].set_title('InVehSt')
axs[2].set_xlabel(None)
plt.xlabel("Anzahl durchgelassener Fahrzeuge pro Ampelphase")

plt.tight_layout()
plt.savefig('', format="pdf")
plt.show()

