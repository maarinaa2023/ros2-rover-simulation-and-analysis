import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

# Obtener modulo rosbag
try:
    import rosbag2_py
    from rclpy.serialization import deserialize_message
    from rosidl_runtime_py.utilities import get_message
except ImportError as e:
    print("\n[ERROR] No se pudo importar rosbag2_py / rclpy.")
    print("Asegúrate de tener el entorno de ROS 2 cargado:")
    print("    source /opt/ros/humble/setup.bash")
    print(f"\nDetalle: {e}\n")
    sys.exit(1)

# Visual
DARK_BG = "#0d0f14"
PANEL_BG = "#13161e"
ACCENT1 = "#00e5ff"
ACCENT2 = "#ff4d6d"
ACCENT3 = "#76ff7a"
ACCENT4 = "#ffcc00"
TEXT = "#dde3f0"
GRID_C = "#1f2535"

JOINT_COLORS = [ACCENT1, ACCENT2, ACCENT3, ACCENT4,
                "#bf9cff", "#ff8c42", "#4de8b2", "#ff79c6"]

matplotlib.rcParams.update({
    "figure.facecolor": DARK_BG,   "axes.facecolor":   PANEL_BG,
    "axes.edgecolor":   "#2a3050", "axes.labelcolor":  TEXT,
    "axes.titlecolor":  TEXT,      "xtick.color":      TEXT,
    "ytick.color":      TEXT,      "text.color":       TEXT,
    "grid.color":       GRID_C,    "grid.linestyle":   "--",
    "grid.linewidth":   0.6,       "legend.facecolor": PANEL_BG,
    "legend.edgecolor": "#2a3050", "legend.labelcolor":TEXT,
    "font.family":      "monospace", "font.size":      10,
})

# Lectura del bag con ayuda del modulo
def open_reader(bag_path: str):
    """Intenta abrir con sqlite3, sino con mcap si falla."""
    converter = rosbag2_py.ConverterOptions(
        input_serialization_format="cdr",
        output_serialization_format="cdr"
    )
    for storage_id in ("sqlite3", "mcap"):
        try:
            opts = rosbag2_py.StorageOptions(uri=bag_path, storage_id=storage_id)
            reader = rosbag2_py.SequentialReader()
            reader.open(opts, converter)
            print(f"[INFO] Bag abierto con storage_id='{storage_id}'")
            return reader
        except Exception as e:
            print(f"[WARN] storage_id='{storage_id}' falló: {e}")
    raise RuntimeError(f"No se pudo abrir el bag: {bag_path}")


def read_bag(bag_path: str):
    """Lee el bag y devuelve datos estructurados."""

    bag_path = str(Path(bag_path).resolve())
    reader = open_reader(bag_path)

    # mapa topic nos da el tipo de mensaje
    type_map = {t.name: t.type for t in reader.get_all_topics_and_types()}
    print(f"[INFO] Topics disponibles: {sorted(type_map.keys())}")

    for wanted in ["/cmd_vel", "/imu/data", "/joint_states"]:
        if wanted not in type_map:
            print(f"[WARN] Topic no encontrado en el bag: {wanted}")

    joint_raw, imu_raw, cmd_raw = [], [], []

    while reader.has_next():
        topic, data, t_ns = reader.read_next()
        msg_type = type_map.get(topic)
        if msg_type is None:
            continue
        try:
            msg = deserialize_message(data, get_message(msg_type))
        except Exception:
            continue

        t_s = t_ns * 1e-9
        if topic == "/joint_states":
            joint_raw.append((t_s, msg))
        elif topic == "/imu/data":
            imu_raw.append((t_s, msg))
        elif topic == "/cmd_vel":
            cmd_raw.append((t_s, msg))

    joint_data = {}
    if joint_raw:
        t0 = joint_raw[0][0]
        for t_s, msg in joint_raw:
            for i, jname in enumerate(msg.name):
                if jname not in joint_data:
                    joint_data[jname] = {"t": [], "pos": [], "vel": [], "eff": []}
                d = joint_data[jname]
                d["t"].append(t_s - t0)
                d["pos"].append(float(msg.position[i]) if i < len(msg.position) else 0.0)
                d["vel"].append(float(msg.velocity[i]) if i < len(msg.velocity) else 0.0)
                d["eff"].append(float(msg.effort[i])   if i < len(msg.effort)   else 0.0)

    imu_data = {"t": [], "ax": [], "ay": [], "az": []}
    if imu_raw:
        t0 = imu_raw[0][0]
        for t_s, msg in imu_raw:
            imu_data["t"].append(t_s - t0)
            imu_data["ax"].append(float(msg.linear_acceleration.x))
            imu_data["ay"].append(float(msg.linear_acceleration.y))
            imu_data["az"].append(float(msg.linear_acceleration.z))

    cmd_data = {"t": [], "vx": [], "wz": []}
    if cmd_raw:
        t0 = cmd_raw[0][0]
        for t_s, msg in cmd_raw:
            cmd_data["t"].append(t_s - t0)
            cmd_data["vx"].append(float(msg.linear.x))
            cmd_data["wz"].append(float(msg.angular.z))

    return joint_data, imu_data, cmd_data

def _no_data(ax, msg="Sin datos"):
    ax.text(0.5, 0.5, msg, ha="center", va="center",
            transform=ax.transAxes, color=ACCENT2, fontsize=12)


def plot_all(joint_data, imu_data, cmd_data, out_path="rover_plots.png"):

    fig = plt.figure(figsize=(18, 14), facecolor=DARK_BG)
    fig.suptitle("ROVER — Análisis de Datos",
                 fontsize=18, fontweight="bold", color=ACCENT1,
                 y=0.97, fontfamily="monospace")

    gs = gridspec.GridSpec(3, 1, figure=fig,
                           hspace=0.55, top=0.90, bottom=0.06,
                           left=0.05, right=0.97)

    ax1 = fig.add_subplot(gs[0])
    ax1.set_title("1. Posición de las Ruedas vs Tiempo  [/joint_states → position]",
                  fontsize=11, pad=8, color=ACCENT1)
    ax1.set_xlabel("Tiempo (s)")
    ax1.set_ylabel("Posición (rad)")
    ax1.grid(True, alpha=0.4)

    if joint_data:
        for idx, (jname, jv) in enumerate(joint_data.items()):
            color = JOINT_COLORS[idx % len(JOINT_COLORS)]
            t = np.array(jv["t"])
            pos = np.array(jv["pos"])
            if len(t):
                ax1.plot(t, pos, lw=1.5, color=color, label=jname, alpha=0.9)
        ax1.legend(loc="lower left", fontsize=8,
                   ncol=max(1, len(joint_data) // 4))
    else:
        _no_data(ax1, "Sin datos de /joint_states")

    ax2 = fig.add_subplot(gs[1])
    ax2.set_title("2. Aceleración Lineal vs Tiempo  [/imu/data → linear_acceleration]",
                  fontsize=11, pad=8, color=ACCENT3)
    ax2.set_xlabel("Tiempo (s)")
    ax2.set_ylabel("Aceleración (m/s²)")
    ax2.grid(True, alpha=0.4)

    if imu_data["t"]:
        t  = np.array(imu_data["t"])
        ax = np.array(imu_data["ax"])
        ay = np.array(imu_data["ay"])
        az = np.array(imu_data["az"])
        mag = np.sqrt(ax**2 + ay**2 + az**2)
        ax2.plot(t, ax,  color=ACCENT1, lw=1.4, label="aX",       alpha=0.9)
        ax2.plot(t, ay,  color=ACCENT2, lw=1.4, label="aY",       alpha=0.9)
        ax2.plot(t, az,  color=ACCENT3, lw=1.4, label="aZ",       alpha=0.9)
        ax2.plot(t, mag, color=ACCENT4, lw=2.0, ls="--",
                 label="|a| total", alpha=0.85)
        ax2.legend(loc="upper right", fontsize=9)
    else:
        _no_data(ax2, "Sin datos de /imu/data")

    ax3 = fig.add_subplot(gs[2])
    ax3.set_title("3. Gasto ≈ |vel x effort| por Rueda vs Tiempo  [/joint_states]",
                  fontsize=11, pad=8, color=ACCENT4)
    ax3.set_xlabel("Tiempo (s)")
    ax3.set_ylabel("Gasto (W equiv.)")
    ax3.grid(True, alpha=0.4)

    if joint_data:
        t_ref = None
        total_pwr = None

        for idx, (jname, jv) in enumerate(joint_data.items()):
            color = JOINT_COLORS[idx % len(JOINT_COLORS)]
            t   = np.array(jv["t"])
            vel = np.array(jv["vel"])
            eff = np.array(jv["eff"])
            pwr = np.abs(vel * eff)

            if len(t):
                ax3.plot(t, pwr, lw=1.2, color=color, label=jname, alpha=0.75)
                if t_ref is None:
                    t_ref = t
                    total_pwr = pwr.copy()
                else:
                    total_pwr += np.interp(t_ref, t, pwr, left=0, right=0)

        if total_pwr is not None:
            ax3.plot(t_ref, total_pwr, color="white", lw=2.2,
                     label="Gasto TOTAL", zorder=5)

        # eje secundario: velocidad lineal de cmd_vel
        if cmd_data["t"]:
            ax3b = ax3.twinx()
            ax3b.set_ylabel("cmd_vel linear.x (m/s)", color=ACCENT2)
            ax3b.tick_params(axis="y", labelcolor=ACCENT2)
            ax3b.plot(cmd_data["t"], cmd_data["vx"],
                      color=ACCENT2, lw=1.5, ls=":",
                      label="cmd_vel vx", alpha=0.85)
            ax3b.legend(loc="upper left", fontsize=8)

        ax3.legend(loc="upper right", fontsize=8,
                   ncol=max(1, len(joint_data) // 4))
    else:
        _no_data(ax3, "Sin datos de /joint_states")

    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    print(f"\n[OK] Gráfica guardada en: {out_path}")
    plt.show()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    bag_path = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else "rover_plots.png"

    print(f"[INFO] Leyendo bag: {bag_path}")
    joint_data, imu_data, cmd_data = read_bag(bag_path)

    print(f"[INFO] Joints encontrados : {list(joint_data.keys())}")
    print(f"[INFO] Muestras IMU       : {len(imu_data['t'])}")
    print(f"[INFO] Muestras cmd_vel   : {len(cmd_data['t'])}")

    print("[INFO] Generando gráficas...")
    plot_all(joint_data, imu_data, cmd_data, out_path=out_file)


if __name__ == "__main__":
    main()
