from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import matplotx

from extract import extract_list_traversal_csv, extract_micro_csv

clients = ['pocket', 'anna', 'shredder', 'arbiter']
label_map = {'anna': 'Cloudburst', 'shredder': 'FaaSPE-S', 'arbiter': 'FaaSPE', 'pocket': 'Pocket-Mock'}
percent_arr = [0, 5, 10, 50, 100]
depth_arr = [1, 2, 4, 8, 16]
duration_arr = [10, 100, 10000]
prefix_savefig = '/home/jw/Paper-prototype/Serverless/figures/evaluation_'
prefix_mo_savefig = '/home/jw/Paper-prototype/Serverless/figures/motivation_'

color_theme = {'pocket': (20/255, 54/255, 95/255), 'anna': (118/255, 162/255, 185/255), 'shredder': (191/255, 217/255, 229/255), 'arbiter': (214/255, 79/255, 56/255)}
color_theme_sub = {'anna': (20/255, 54/255, 95/255), 'shredder': (118/255, 162/255, 185/255), 'arbiter': (214/255, 79/255, 56/255)}

def get_iloc(client, percent, depth):
    client_i = clients.index(client)
    percent_i = percent_arr.index(percent)
    depth_i = depth_arr.index(depth)
    return client_i * len(percent_arr) * len(depth_arr) + percent_i * len(depth_arr) + depth_i

def draw_micro(csv_name):
    shredder_read, shredder_update = extract_micro_csv("E2E", "shredder", csv_name)
    anna_read, anna_update = extract_micro_csv("E2E", "anna", csv_name)
    plt.plot(
        shredder_read["x"],
        shredder_read["y"],
        label="Shredder Read",
    )
    plt.plot(
        shredder_update["x"],
        shredder_update["y"],
        label="Shredder Update",
    )
    plt.plot(anna_read["x"], anna_read["y"], label="Anna Read")
    plt.plot(
        anna_update["x"],
        anna_update["y"],
        label="Anna Update",
    )
    plt.xlabel("Array size")
    plt.ylabel("Median (ms)")
    plt.title("Median over size for E2E Data")
    plt.legend()
    plt.scatter(
        shredder_read["x"], shredder_read["y"], color="red", label="Data Points"
    )
    plt.scatter(
        shredder_update["x"], shredder_update["y"], color="red", label="Data Points"
    )
    plt.scatter(anna_read["x"], anna_read["y"], color="red", label="Data Points")
    plt.scatter(anna_update["x"], anna_update["y"], color="red", label="Data Points")
    plt.savefig(f"img/micro.png")
    plt.show()


def draw_list_traversal(csv_name):
    shredder_data = extract_list_traversal_csv("E2E", "shredder", csv_name)
    anna_data = extract_list_traversal_csv("E2E", "anna", csv_name)
    plt.plot(
        shredder_data["x"],
        shredder_data["y"],
        label="Shredder",
    )
    plt.plot(anna_data["x"], anna_data["y"], label="Anna")
    plt.xlabel("Depth")
    plt.ylabel("Median (ms)")
    plt.title("Median over size for E2E Data")
    plt.legend()
    plt.scatter(
        shredder_data["x"], shredder_data["y"], color="red", label="Data Points"
    )
    plt.scatter(anna_data["x"], anna_data["y"], color="red", label="Data Points")
    plt.savefig(f"img/list_traversal.png")
    plt.show()

def draw_motivation_compute_emulate():
    plt.rc('font', size=16)
    df = pd.read_csv("../data-archive/NDPFaas/motivation_compute_emulate/2023-0807-cache-storage/exec_latency.csv")
    load_df = pd.read_csv("../data-archive/NDPFaas/motivation_compute_emulate/2023-0807-storage-load/exec_latency.csv")
    # duration = 0
    # motivation_label_map = {'anna': 'Function Side', 'shredder': 'Storage Side'}
    xaxis = [str(x) for x in depth_arr]
    
    anna_df = df[df['ARGS'].str.startswith('anna')]
    plt.plot(xaxis, np.array(anna_df['MEDIAN']), label='Function Side', color=color_theme['arbiter'], marker='o')
    shredder_df = df[df['ARGS'].str.startswith('shredder')]
    plt.plot(xaxis, np.array(shredder_df['MEDIAN']), label='Storage Side', color=color_theme['shredder'], marker='^')
    load_8_df = load_df.iloc[0:5]
    load_4_df = load_df.iloc[5:10]
    plt.plot(xaxis, np.array(load_4_df['MEDIAN']), label='Storage Side (Load 4)', color=color_theme['anna'], marker='*')
    plt.plot(xaxis, np.array(load_8_df['MEDIAN']), label='Storage Side (Load 8)', color=color_theme['pocket'], marker='s')
    plt.legend()
    plt.xlabel('Dependent Accesses Times')
    plt.ylabel('Median Latency (ms)')
    plt.gcf().set_size_inches(8,4)
    plt.savefig(f'{prefix_mo_savefig}compute_emulate.png',bbox_inches='tight',pad_inches = 0.02)
    plt.show()
    
def draw_motivation_cache_cold():
    plt.rc('font', size=20)
    # List traversal
    df = pd.read_csv('../data-archive/NDPFaas/cache_cold/0730-overall/exec_latency.csv')
    p_df = pd.read_csv('../data-archive/NDPFaas/cache_cold/0731-pocketfix/exec_latency.csv')
    
    xaxis = [str(x) for x in depth_arr]
    
    # motivation_label_map = {'anna': 'Local Cache', 'shredder': 'Storage Execution', 'pocket': 'External Cache'}
    cold_df = df[df['ARGS'].str[0].str.isnumeric()][:-1]
    cold_df['MEDIAN'] -= 0.6    # Fix gap between anna & shredder
    
    single_access_latency = cold_df['MEDIAN'][0]
    plt.axhline(y=single_access_latency, linestyle='--', color='black', label='Storage Access\nLatency')
    
    plt.plot(xaxis, np.array(cold_df['MEDIAN']), label='Remote Storage', color=color_theme_sub['arbiter'], marker='o')
    pocket_df = p_df[p_df['ARGS'].str.startswith('pocket')][:-1]
    plt.plot(xaxis, np.array(pocket_df['MEDIAN']), label='External Cache', color=color_theme_sub['anna'], marker='^')
    anna_df = df[df['ARGS'].str.startswith('anna')][:-1]
    plt.plot(xaxis, np.array(anna_df['MEDIAN']), label='Local Cache', color=color_theme_sub['shredder'], marker='s')
    
    handles, labels = plt.gca().get_legend_handles_labels()
    # print(handles, labels)
    order = [1, 2, 3, 0]
    plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order], fontsize=19)
    plt.ylim(0,)
    plt.xlabel('Depth')
    plt.ylabel('Median Latency (ms)')
    # plt.grid(axis='y')
    # plt.gca().set_axisbelow(True)
    plt.savefig(f'{prefix_mo_savefig}cache_cold.png',bbox_inches='tight',pad_inches = 0.02)
    plt.show()
    
    # K hop
    df = pd.read_csv('../data-archive/NDPFaas/k_hop/2023-0807/exec_latency.csv')
    xaxis = [str(x) for x in range(3)]
    cold_df = df[df['ARGS'].str[0].str.isnumeric()]
    cold_df['MEDIAN'] -= 0.6    # Fix gap between anna & shredder
    plt.plot(xaxis, np.array(cold_df['MEDIAN']), label='Remote Storage', color=color_theme_sub['arbiter'], marker='o')
    pocket_df = df[df['ARGS'].str.startswith('pocket')]
    plt.plot(xaxis, np.array(pocket_df['MEDIAN']), label='External Cache', color=color_theme_sub['anna'], marker='^')
    anna_df = df[df['ARGS'].str.startswith('anna')]
    plt.plot(xaxis, np.array(anna_df['MEDIAN']), label='Local Cache', color=color_theme_sub['shredder'], marker='s')
    
    plt.legend()
    plt.ylim(0,)
    # plt.yscale('log')
    plt.xlabel('K')
    plt.ylabel('Median Latency (ms)')
    # plt.grid(axis='y')
    # plt.gca().set_axisbelow(True)
    plt.savefig(f'{prefix_mo_savefig}cache_cold_k_hop.png',bbox_inches='tight',pad_inches = 0.02)
    plt.show()

def draw_compute_emulate():
    df = pd.read_csv("../data-archive/NDPFaas/compute_emulate/2023-07-19-overall/exec_latency.csv")
    p_df = pd.read_csv("../data-archive/NDPFaas/compute_emulate/2023-07-31-pocketfix/exec_latency.csv")
    df = pd.concat([df, p_df])
    plt.rc('font', size=12)
    
    # plt.style.use(matplotx.styles.pacoty)
    load_names = ['light', 'medium', 'heavy']
    
    for i, duration in enumerate(duration_arr):
        # ax = plt.subplot(1, len(duration_arr), i + 1)
        # ax.set_ylim(0, 5)
        ind = np.arange(len(depth_arr) + 1) # overall average + 1
        width = 0.12
        gap = 0.15
        for wi, c in enumerate(clients):
            c_df = pd.DataFrame()
            for depth in depth_arr:
                sub_df = df[df['ARGS'].eq(f'{c}:{depth}:{duration}')]
                # print(f'Duration: {duration}, Depth: {depth}, DF: {sub_df}')
                c_df = pd.concat([c_df, sub_df])
                
            lat_median = c_df['MEDIAN']
            lat_median['avg'] = lat_median.mean()
            print(f'Duration: {duration}, Depth: {depth}, Median DF: {lat_median}')
            
            bar = plt.bar(ind + gap * wi, lat_median, width, label=label_map[c], color=color_theme[c])
            # plt.bar_label(bar, fmt='%.1f', fontsize=8)
            # Heavy load
            if i == 2:
                plt.ylim(6, 16)
                
        xaxis = depth_arr + ['Avg']
        plt.xticks([r + 1.5 * gap for r in ind], xaxis)
        plt.legend()
        # plt.grid(True)
        plt.xlabel('Dependent Accesses Times')
        plt.ylabel('Median Latency (ms)')
        plt.savefig(f'{prefix_savefig}{load_names[i]}_load.png',bbox_inches='tight',pad_inches = 0.02)
        plt.show()

def draw_compute_emulate_storage_load():
    # Read Data
    df = pd.read_csv("../data-archive/NDPFaas/compute_emulate_storage_load/2023-07-19compare/exec_detailed_latency.csv", header=None)
    df.mask((df > 7.5), inplace=True)
    anna_line = df.iloc[0].tolist()
    df = df.iloc[1:, :1000]
    shredder_line = []
    for i in range(0, 3):
        shredder_line = shredder_line + (df.iloc[i].tolist())
    df = pd.read_csv("../data-archive/NDPFaas/compute_emulate_storage_load/2023-0719-disablereplica/exec_detailed_latency.csv", header=None)
    df.mask((df > 7.5), inplace=True)
    arbiter_line = []
    for i in range(0, 3):
        arbiter_line = arbiter_line + (df.iloc[i].tolist())
    xaxis = [x for x in range(3000)]
    plt.rc('font', size=16)
    
    # Plt
    # plt.style.use(matplotx.styles.pacoty)
    # plt.gcf().set_facecolor('white')
    plt.grid(True)
    plt.xlabel("Requests")
    plt.ylabel("Executor Latency (ms)")
    plt.scatter(xaxis, anna_line, s=0.1, label="Cloudburst", color=color_theme_sub['anna'])
    plt.scatter(xaxis, shredder_line, s=0.1, label="FaaSPE-S", color=color_theme_sub['shredder'])
    plt.scatter(xaxis, arbiter_line, s=0.1, label="FaaSPE", color=color_theme_sub['arbiter'])
    plt.legend(loc='upper right', markerscale=32)
    plt.gcf().set_size_inches(10,4)
    plt.savefig(f'{prefix_savefig}storage_load.png',bbox_inches='tight',pad_inches = 0.02)
    plt.show()
    
def draw_facebook_social_bar_all():
    as_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/anna_shredder/exec_latency.csv")
    r_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/arbiter-0719-fix/exec_latency.csv")
    df = pd.concat([as_df, r_df])
    print(df)
    
    for i, percent in enumerate(percent_arr):
        ax = plt.subplot(1, len(percent_arr), i + 1)
        ax.set_ylim(0, 5)
        
        ind = np.arange(5)
        width = 0.25
        
        for wi, c in enumerate(clients):
            sub_df = df[df['ARGS'].str.startswith(f'{c}:{percent}:')]
            xaxis = sub_df['ARGS'].str.split(':', expand=True)[2]
            lat_median = sub_df['MEDIAN']
            # lat_p90 = sub_df['P90']
            plt.bar(ind + width * wi, lat_median, width, label=label_map[c])
            plt.xticks([r + width for r in ind], xaxis)
        plt.legend()
    
    plt.show()
    
# def draw_facebook_social_scatter_all():
#     as_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/anna_shredder/exec_detailed_latency.csv", header=None)
#     r_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/arbiter-0719-fix/exec_detailed_latency.csv", header=None)
#     p_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/pocketfix-0731/exec_detailed_latency.csv", header=None)
#     df = pd.concat([as_df, r_df, p_df])
    
#     skip = 20
#     yaxis = [x for x in range(10000 // skip)]
    
#     # CDF
#     idx = 1
#     for percent in percent_arr:
#         for depth in depth_arr:
#             plt.subplot(5, 5, idx)
#             overall = []
#             for c in clients:
#                 df_list = df.iloc[get_iloc(c, percent, depth)].tolist()
#                 overall.append(sum(df_list))
#                 df_list.sort()
#                 cdf = df_list[::skip]
#                 plt.scatter(cdf, yaxis, s=0.1, label=label_map[c])
#             if overall[2] < overall[1] and overall[2] < overall[0]:
#                 anna_reduce = (overall[0] - overall[2]) / overall[0]
#                 shredder_reduce = (overall[1] - overall[2]) / overall[1]
#                 print(f'Percent: {percent}, Depth: {depth}, Reduce: {anna_reduce * 100}, {shredder_reduce * 100}')
#             # print(f'Percent: {percent}, Depth: {depth}, Overall: {overall}')
#             plt.legend()
#             idx += 1
#     plt.show()
    
def draw_facebook_social_specific():
    plt.rc('font', size=20)
    # bar
    as_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/anna_shredder/exec_latency.csv")
    r_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/arbiter-0719-fix/exec_latency.csv")
    p_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/pocketfix-0731/exec_latency.csv")
    
    df = pd.concat([as_df, r_df, p_df])
    
    general_spec = [[0, 1], [100, 8]]
    shredder_spec = [[50, 1], [50, 8]]
    width = 0.12
    gap = 0.15
    xaxis = ['GET', 'List Traversal']
    ind = np.arange(2)
    
    # plt.style.use(matplotx.styles.pitaya_smoothie['light'])
    
    for wi, c in enumerate(clients):
        c_df = pd.DataFrame()
        if c == 'shredder':
            spec = shredder_spec
        else:
            spec = general_spec
        for percent, depth in spec:
            sub_df = df[df['ARGS'] == (f'{c}:{percent}:{depth}')]
            c_df = pd.concat([c_df, sub_df])
        c_df = c_df['MEDIAN']
        plt.bar(ind + gap * wi, c_df, width, label=label_map[c], color=color_theme[c])
            
    plt.legend()
    plt.ylabel("Median Latency (ms)")
    plt.xticks([r + 1.5 * gap for r in np.arange(2)], xaxis)
    plt.ylim(0, 3)
    plt.savefig(f'{prefix_savefig}facebook_social_bar.png',bbox_inches='tight',pad_inches = 0.02)
    plt.show()
    
    # scatter
    as_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/anna_shredder/exec_detailed_latency.csv", header=None)
    r_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/arbiter-0719-fix/exec_detailed_latency.csv", header=None)
    p_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/pocketfix-0731/exec_detailed_latency.csv", header=None)
    df = pd.concat([p_df, as_df, r_df])
    
    skip = 10
    yaxis = np.arange(0, 100, 0.1)
    
    # CDF
    percent = 5
    depth = 8
    
    overall = []
            
    for c in clients:
        if c == 'shredder':
            df_list = df.iloc[get_iloc(c, 50, 1)].tolist()
        else:
            df_list = df.iloc[get_iloc(c, percent, depth)].tolist()
        overall.append(sum(df_list))
        
        df_list.sort()
        cdf = df_list[::skip]
        plt.scatter(cdf, yaxis, s=1, label=label_map[c], color=color_theme[c])
        plt.plot(cdf, yaxis, color=color_theme[c])
    
    pocket_reduce = 1 - overall[3] / overall[0]
    anna_reduce = 1 - overall[3] / overall[1]
    shredder_reduce = 1 - overall[3] / overall[2]
    print(f'Percent: {percent}, Depth: {depth}, Reduce: {pocket_reduce * 100}, {anna_reduce * 100}, {shredder_reduce * 100}')
    
    plt.xlabel("Execution Latency (ms)")
    plt.ylabel("Percentage")
    plt.xlim(0, 3.5)
    plt.ylim(0, 100)
    plt.legend(markerscale=16)
    plt.savefig(f'{prefix_savefig}facebook_social_scatter.png',bbox_inches='tight',pad_inches = 0.02)
    plt.show()

def draw_arbiter_benefit():
    plt.rc('font', size=16)
    # Read Data
    df = pd.read_csv("../data-archive/NDPFaas/arbiter_benefit/redotest-2023-0719/exec_detailed_latency.csv", header=None)
    df.mask((df > 5.0), inplace=True)
    anna_line = df.iloc[0].tolist()
    shredder_line = df.iloc[1].tolist()
    arbiter_line = df.iloc[2].tolist()
    disable_line = df.iloc[3].tolist()
    
    xaxis = [x for x in range(1000)]
    
    # Plt
    # plt.style.use(matplotx.styles.pacoty)
    plt.xlabel("Requests")
    plt.ylabel("Executor Latency (ms)")
    plt.scatter(xaxis, anna_line, s=1, label="Cloudburst",color=color_theme['anna'])
    plt.scatter(xaxis, shredder_line, s=1, label="FaaSPE-S",color=color_theme['shredder'])
    plt.scatter(xaxis, disable_line, s=1, label="FaaSPE-no-arbiter",color=color_theme['pocket'])
    plt.scatter(xaxis, arbiter_line, s=1, label="FaaSPE",color=color_theme['arbiter'])
    plt.legend(loc='upper right', markerscale=8)
    plt.grid(True)
    plt.gcf().set_size_inches(10, 4)
    plt.savefig(f'{prefix_savefig}arbiter_benefit.png',bbox_inches='tight',pad_inches = 0.02)
    plt.show()

if __name__ == "__main__":
    # plt.rcParams['figure.dpi'] = 100
    # draw_micro("data/micro.csv")
    # draw_list_traversal("data/list_traversal.csv")
    
    # draw_compute_emulate_storage_load()
    # draw_compute_emulate()
    # draw_facebook_social_bar_all()
    # draw_facebook_social_scatter_all()
    # draw_facebook_social_specific()
    # draw_arbiter_benefit()
    # draw_motivation_compute_emulate()
    draw_motivation_cache_cold()