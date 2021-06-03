from matplotlib import pyplot as plt
import pandas as pd

def alert_filter(smoothed_data):
    
    df_alert = smoothed_data[smoothed_data['alert'] == True]

    return df_alert['activity']

def generate_plots(smoothed_data, cow_id):
    
    xticks = list(smoothed_data.index.strftime('%Y-%m-%d').unique())

    alert_series = alert_filter(smoothed_data)

    plt.style.use('ggplot')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(35, 15), sharex = True)

    ax1.plot(smoothed_data['activity'], label = 'Activity', alpha = 0.6, linewidth = 1.5, color = '#ffa600')
    ax1.plot(smoothed_data['exp_smooth'], label = 'Smoothed', linewidth = 3.5, color = '#003f5c')
    ax1.scatter(alert_series.index, alert_series, label = 'Alert', color = '#f11827')
    ax2.plot(smoothed_data['residue'], linewidth = 3, color = '#003f5c')

    ax1.tick_params('both', labelsize = 24, labelcolor = 'black', grid_color = 'black', grid_alpha = 0.5)
    ax2.tick_params('both', labelsize = 24, labelcolor = 'black', grid_color = 'black', grid_alpha = 0.5)

    ax1.legend(fontsize = 26, frameon = True, framealpha = 0.6, facecolor = 'white', edgecolor = 'black', loc = 'upper right')

    ax1.set_title(f'Cow {cow_id} Analysis', fontsize = 30)
    ax1.set_ylabel('Cumulative 24h Activity', fontsize = 28, labelpad = 16, color = 'black')
    ax2.set_ylabel('Residue', fontsize = 28, labelpad = 10, color = 'black')
    ax2.set_xlabel('Dates', fontsize = 28, labelpad = 16, color = 'black')

    plt.xticks(xticks, rotation = 70)
    plt.tight_layout()
    plt.savefig(f'cow_{cow_id}_report.png')
    plt.plot()
