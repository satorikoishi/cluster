from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import matplotx

from extract import extract_list_traversal_csv, extract_micro_csv

clients = ['anna', 'shredder', 'arbiter', 'pocket']
label_map = {'anna': 'Cloudburst', 'shredder': 'FaaSPE-S', 'arbiter': 'FaaSPE', 'pocket': 'Pocket-Mock'}
percent_arr = [0, 5, 10, 50, 100]
depth_arr = [1, 2, 4, 8, 16]
duration_arr = [10, 100, 10000]
prefix_savefig = '/home/jw/Paper-prototype/Serverless/figures/evaluation_'
prefix_mo_savefig = '/home/jw/Paper-prototype/Serverless/figures/motivation_'

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
    df = pd.read_csv("../data-archive/NDPFaas/compute_emulate/2023-07-19-overall/exec_latency.csv")
    duration = 0
    motivation_label_map = {'anna': 'Function Side', 'shredder': 'Storage Side'}
    xaxis = [str(x) for x in depth_arr]
    
    for c in ['anna', 'shredder']:
        c_df = pd.DataFrame()
        for depth in depth_arr:
            sub_df = df[df['ARGS'].eq(f'{c}:{depth}:{duration}')]
            c_df = pd.concat([c_df, sub_df])
        
        lat_median = c_df['MEDIAN']
        plt.plot(xaxis, np.array(lat_median), label=motivation_label_map[c])
    plt.legend()
    plt.xlabel('Dependent Accesses Times')
    plt.ylabel('Median Latency (ms)')
    plt.savefig(f'{prefix_mo_savefig}compute_emulate.png')
    plt.show()

def draw_compute_emulate():
    df = pd.read_csv("../data-archive/NDPFaas/compute_emulate/2023-07-19-overall/exec_latency.csv")
    p_df = pd.read_csv("../data-archive/NDPFaas/compute_emulate/2023-07-30-pocket/exec_latency.csv")
    df = pd.concat([df, p_df])
    
    plt.style.use(matplotx.styles.pacoty)
    load_names = ['light', 'medium', 'heavy']
    
    for i, duration in enumerate(duration_arr):
        # ax = plt.subplot(1, len(duration_arr), i + 1)
        # ax.set_ylim(0, 5)
        ind = np.arange(len(depth_arr) + 1) # overall average + 1
        width = 0.15
        for wi, c in enumerate(clients):
            c_df = pd.DataFrame()
            for depth in depth_arr:
                sub_df = df[df['ARGS'].eq(f'{c}:{depth}:{duration}')]
                print(f'Duration: {duration}, Depth: {depth}, DF: {sub_df}')
                c_df = pd.concat([c_df, sub_df])
                
            lat_median = c_df['MEDIAN']
            lat_median['avg'] = lat_median.mean()
            print(f'Duration: {duration}, Depth: {depth}, Median DF: {lat_median}')
            
            plt.bar(ind + width * wi, lat_median, width, label=label_map[c])
                
        xaxis = depth_arr + ['Avg']
        plt.xticks([r + width for r in ind], xaxis)
        plt.legend()
        plt.xlabel('Dependent Accesses Times')
        plt.ylabel('Median Latency (ms)')
        plt.savefig(f'{prefix_savefig}{load_names[i]}_load.png')
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
    
    # Plt
    plt.style.use(matplotx.styles.pacoty)
    plt.xlabel("Requests")
    plt.ylabel("Executor Latency (ms)")
    plt.scatter(xaxis, arbiter_line, s=0.1, label="FaaSPE")
    plt.scatter(xaxis, anna_line, s=0.1, label="Cloudburst")
    plt.scatter(xaxis, shredder_line, s=0.1, label="Cloudburst-S")
    plt.legend(loc='upper right', markerscale=8)
    plt.savefig(f'{prefix_savefig}storage_load.png')
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
    
def draw_facebook_social_scatter_all():
    as_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/anna_shredder/exec_detailed_latency.csv", header=None)
    r_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/arbiter-0719-fix/exec_detailed_latency.csv", header=None)
    p_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/pocket-0730/exec_detailed_latency.csv", header=None)
    df = pd.concat([as_df, r_df, p_df])
    
    skip = 20
    yaxis = [x for x in range(10000 // skip)]
    
    # CDF
    idx = 1
    for percent in percent_arr:
        for depth in depth_arr:
            plt.subplot(5, 5, idx)
            overall = []
            for c in clients:
                df_list = df.iloc[get_iloc(c, percent, depth)].tolist()
                overall.append(sum(df_list))
                df_list.sort()
                cdf = df_list[::skip]
                plt.scatter(cdf, yaxis, s=0.1, label=label_map[c])
            if overall[2] < overall[1] and overall[2] < overall[0]:
                anna_reduce = (overall[0] - overall[2]) / overall[0]
                shredder_reduce = (overall[1] - overall[2]) / overall[1]
                print(f'Percent: {percent}, Depth: {depth}, Reduce: {anna_reduce * 100}, {shredder_reduce * 100}')
            # print(f'Percent: {percent}, Depth: {depth}, Overall: {overall}')
            plt.legend()
            idx += 1
    plt.show()
    
def draw_facebook_social_specific():
    # bar
    as_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/anna_shredder/exec_latency.csv")
    r_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/arbiter-0719-fix/exec_latency.csv")
    p_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/pocket-0730/exec_latency.csv")
    
    df = pd.concat([as_df, r_df, p_df])
    
    spec = [[0, 1], [100, 8]]
    width = 0.2
    xaxis = ['GET', 'List_traversal']
    ind = np.arange(2)
    
    plt.style.use(matplotx.styles.pitaya_smoothie['light'])
    
    for wi, c in enumerate(clients):
        c_df = pd.DataFrame()
        for percent, depth in spec:
            sub_df = df[df['ARGS'] == (f'{c}:{percent}:{depth}')]
            c_df = pd.concat([c_df, sub_df])
        c_df = c_df['MEDIAN']
        plt.bar(ind + width * wi, c_df, width, label=label_map[c])
            
    plt.legend()
    plt.ylabel("Median Latency (ms)")
    plt.xticks([r + width for r in np.arange(2)], xaxis)
    plt.ylim(0, 2)
    plt.savefig(f'{prefix_savefig}facebook_social_bar.png')
    plt.show()
    
    # scatter
    as_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/anna_shredder/exec_detailed_latency.csv", header=None)
    r_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/arbiter-0719-fix/exec_detailed_latency.csv", header=None)
    p_df = pd.read_csv("../data-archive/NDPFaas/facebook_social/pocket-0730/exec_detailed_latency.csv", header=None)
    df = pd.concat([as_df, r_df, p_df])
    
    skip = 10
    yaxis = np.arange(0, 100, 0.1)
    
    # CDF
    percent = 5
    depth = 8
            
    for c in clients:
        df_list = df.iloc[get_iloc(c, percent, depth)].tolist()
        df_list.sort()
        cdf = df_list[::skip]
        plt.scatter(cdf, yaxis, s=1, label=label_map[c])
    
    plt.xlabel("Execution Latency (ms)")
    plt.ylabel("Percentage")
    plt.xlim(0, 3.5)
    plt.ylim(0, 100)
    plt.legend(markerscale=8)
    plt.savefig(f'{prefix_savefig}facebook_social_scatter.png')
    plt.show()

def draw_arbiter_benefit():
    # Read Data
    df = pd.read_csv("../data-archive/NDPFaas/arbiter_benefit/redotest-2023-0719/exec_detailed_latency.csv", header=None)
    df.mask((df > 5.0), inplace=True)
    anna_line = df.iloc[0].tolist()
    shredder_line = df.iloc[1].tolist()
    arbiter_line = df.iloc[2].tolist()
    disable_line = df.iloc[3].tolist()
    
    xaxis = [x for x in range(1000)]
    
    # Plt
    plt.style.use(matplotx.styles.pacoty)
    plt.xlabel("Requests")
    plt.ylabel("Executor Latency (ms)")
    plt.scatter(xaxis, arbiter_line, s=0.1, label="FaaSPE")
    plt.scatter(xaxis, disable_line, s=0.1, label="FaaSPE-no-arbiter")
    plt.scatter(xaxis, anna_line, s=0.1, label="Cloudburst")
    plt.scatter(xaxis, shredder_line, s=0.1, label="Cloudburst-S")
    plt.legend(loc='upper right', markerscale=8)
    plt.savefig(f'{prefix_savefig}arbiter_benefit.png')
    plt.show()

if __name__ == "__main__":
    # draw_micro("data/micro.csv")
    # draw_list_traversal("data/list_traversal.csv")
    
    # draw_compute_emulate_storage_load()
    draw_compute_emulate()
    # draw_facebook_social_bar_all()
    # draw_facebook_social_scatter_all()
    # draw_facebook_social_specific()
    # draw_arbiter_benefit()
    # draw_motivation_compute_emulate()
    