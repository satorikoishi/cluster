from matplotlib import pyplot as plt

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
    plt.xlabel("Array size")
    plt.ylabel("Median (ms)")
    plt.title("Median over size for E2E Data")
    plt.legend()
    plt.scatter(
        shredder_data["x"], shredder_data["y"], color="red", label="Data Points"
    )
    plt.scatter(anna_data["x"], anna_data["y"], color="red", label="Data Points")
    plt.savefig(f"img/list_traversal.png")
    plt.show()


if __name__ == "__main__":
    draw_micro("data/micro.csv")
    draw_list_traversal("data/list_traversal.csv")
