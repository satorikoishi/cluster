from matplotlib import pyplot as plt
import pandas as pd

from extract import extract_list_traversal_csv, extract_micro_csv


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
    
def draw_compute_emulate():
    pass

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
    plt.xlabel("Requests")
    plt.ylabel("Executor Latency (ms)")
    plt.scatter(xaxis, arbiter_line, s=0.1, label="FaaSPE")
    plt.scatter(xaxis, anna_line, s=0.1, label="Cloudburst")
    plt.scatter(xaxis, shredder_line, s=0.1, label="Cloudburst-S")
    plt.legend(loc='upper right', markerscale=8)
    plt.show()
    
def draw_facebook_social():
    pass

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
    plt.xlabel("Requests")
    plt.ylabel("Executor Latency (ms)")
    plt.scatter(xaxis, arbiter_line, s=0.1, label="FaaSPE")
    plt.scatter(xaxis, disable_line, s=0.1, label="FaaSPE-no-arbiter")
    plt.scatter(xaxis, anna_line, s=0.1, label="Cloudburst")
    plt.scatter(xaxis, shredder_line, s=0.1, label="Cloudburst-S")
    plt.legend(loc='upper right', markerscale=8)
    plt.show()

if __name__ == "__main__":
    # draw_micro("data/micro.csv")
    # draw_list_traversal("data/list_traversal.csv")
    
    # draw_compute_emulate_storage_load()
    draw_compute_emulate()
    draw_facebook_social()
    draw_arbiter_benefit()
    