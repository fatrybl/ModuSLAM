from collections.abc import Iterable

import gtsam
import plotly.graph_objects as go

from src.custom_types.numpy import VectorN
from src.measurement_storage.measurements.imu import (
    ContinuousImu,
    ImuCovariance,
    ImuData,
    ProcessedImu,
)
from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.measurement_storage.measurements.pose_odometry import Odometry
from src.moduslam.frontend_manager.main_graph.data_classes import (
    GraphElement,
    NewVertex,
)
from src.moduslam.frontend_manager.main_graph.edges.combined_imu_odometry import (
    ImuOdometry,
)
from src.moduslam.frontend_manager.main_graph.edges.noise_models import (
    se3_isotropic_noise_model,
)
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.cluster import Cluster
from src.moduslam.map_manager.visualizers.graph_visualizer.connection_objects import (
    Binary,
    Unary,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.data_factory import (
    Data,
    create_data,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.utils import (
    calculate_curve_properties,
    create_cluster_connections_table,
    generate_bezier_curve,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.visualizer_params import (
    BinaryConnectionParams,
    ClusterParams,
    UnaryConnectionParams,
    VertexParams,
    VisualizationParams,
)
from src.utils.auxiliary_dataclasses import Position2D, TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.auxiliary_objects import one_vector3


def draw(data: Data, vis_params: VisualizationParams) -> None:
    """Draws the provided graph data.

    Args:
        data: Graph data to visualize.

        vis_params: Visualization parameters.
    """
    binary_conns = data.binary_connections
    unary_conns = data.unary_connections

    fig = go.Figure()

    draw_clusters_and_vertices(fig, data.clusters, vis_params)

    draw_binary_connections(fig, binary_conns, vis_params.binary_connection_params)

    draw_unary_connections(fig, unary_conns, vis_params.unary_connection_params)

    fig.show()


def set_cluster_positions(clusters: Iterable[Cluster], space: float) -> None:
    """Sets the positions of the clusters.

    Args:
        clusters: Clusters to set positions for.

        space: space between clusters.
    """
    prev_x = 0.0
    for i, cluster in enumerate(clusters):
        cluster.set_position(Position2D(prev_x, 0))
        prev_x += cluster.width + space


def draw_clusters_and_vertices(
    fig: go.Figure, clusters: Iterable[Cluster], vis_params: VisualizationParams
) -> None:
    """Draw each cluster (box) with and vertices (circles).

    Args:
        fig: a figure to draw on.

        clusters: clusters to draw.

        vis_params: visualization parameters.
    """
    set_cluster_positions(clusters, vis_params.between_clusters_space)
    draw_cluster_bbox(fig, clusters, vis_params.cluster_params)
    draw_circles(fig, clusters, vis_params.vertex_params)


def draw_cluster_bbox(
    fig: go.Figure, clusters: Iterable[Cluster], vis_params: ClusterParams
) -> None:
    """Draws bounding box of the cluster.

    Args:
        fig: a figure to draw on.

        clusters: clusters to draw.

        vis_params: visualization parameters.
    """
    for cluster in clusters:
        x, y = cluster.position.x, cluster.position.y

        fig.add_shape(
            type="rect",
            x0=x,
            y0=y,
            x1=x + cluster.width,
            y1=y + cluster.height,
            line=dict(color="black"),
            fillcolor="lightgray",
            opacity=0.5,
        )

        fig.add_annotation(
            x=x + cluster.width / 2,
            y=y - vis_params.label_offset,
            text=cluster.label,
            showarrow=False,
            font=dict(size=vis_params.label_fontsize, color="black"),
            xanchor="center",
            yanchor="top",
        )

        fig.add_annotation(
            x=x + cluster.width / 2,
            y=y - vis_params.label_offset / 2,
            text=cluster.time_range,
            showarrow=False,
            font=dict(size=vis_params.label_fontsize, color="black"),
            xanchor="center",
            yanchor="top",
        )


def draw_circles(fig: go.Figure, clusters: Iterable[Cluster], vis_params: VertexParams) -> None:
    """Draws circles for each cluster using Plotly.

    Args:
        fig: a figure to draw on.

        clusters: clusters to draw.

        vis_params: visualization parameters.
    """
    for cluster in clusters:
        vertices_with_positions = cluster.vertices_with_positions

        for vertex, position in vertices_with_positions.items():
            x, y = position.x, position.y

            fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="markers",
                    marker=dict(
                        size=vertex.radius * 2,
                        color=vis_params.color,
                        line=dict(width=1, color="black"),
                    ),
                    name=vertex.label,
                    showlegend=False,
                )
            )

            fig.add_annotation(
                x=x,
                y=y,
                text=vertex.label,
                showarrow=False,
                font=dict(size=vis_params.label_fontsize, color="black"),
                xanchor="center",
                yanchor="middle",
            )


def draw_binary_connections(
    fig: go.Figure,
    connections: Iterable[Binary],
    vis_params: BinaryConnectionParams,
) -> None:
    """Draws curved connections between clusters using Plotly.

    Args:
        fig: a figure to draw on.

        connections: binary connections between clusters.

        vis_params: visualization parameters.
    """
    connection_counts: dict[tuple[Cluster, Cluster], int] = {}

    for connection in connections:
        pos1, pos2, mid_point = calculate_curve_properties(
            connection, connection_counts, vis_params
        )

        if connection.draw_below:
            pos1.y = pos2.y = connection.source.position.y
            mid_point.y = pos1.y - vis_params.base_offset
            curve_x, curve_y = generate_bezier_curve(pos1, pos2, mid_point, curvature=-0.2)
        else:
            mid_point.y += vis_params.base_offset
            curve_x, curve_y = generate_bezier_curve(pos1, pos2, mid_point)

        plot_curve(fig, curve_x, curve_y, connection, vis_params)


def plot_curve(
    fig: go.Figure,
    curve_x: VectorN,
    curve_y: VectorN,
    connection: Binary,
    vis_params: BinaryConnectionParams,
) -> None:
    """Plots the Bézier curve and labels it using Plotly.

    Args:
        fig: a figure to draw on.

        curve_x: x coordinates of the curve.

        curve_y: y coordinates of the curve.

        connection: the binary connection being drawn.

        vis_params: visualization parameters.
    """
    fig.add_trace(
        go.Scatter(
            x=curve_x,
            y=curve_y,
            mode="lines",
            line=dict(
                color=vis_params.curve_color,
                width=vis_params.curve_lw,
            ),
            opacity=vis_params.curve_alpha,
            hoverinfo="none",
            showlegend=False,
        )
    )

    mid_i = len(curve_x) // 2
    fig.add_annotation(
        x=curve_x[mid_i],
        y=curve_y[mid_i] + vis_params.label_offset,
        text=connection.label,
        showarrow=False,
        font=dict(
            size=vis_params.label_fontsize,
            color=vis_params.label_color,
        ),
        opacity=vis_params.label_alpha,
        xanchor="center",
        yanchor="bottom",
    )


def draw_unary_connections(
    fig: go.Figure,
    connections: Iterable[Unary],
    vis_params: UnaryConnectionParams,
) -> None:
    """Draws ladder-style vertical lines for each cluster.

    Args:
        fig: a figure to draw on.

        connections: Unary connections for clusters.

        vis_params: Visualization parameters.
    """
    cluster_connections = create_cluster_connections_table(connections)

    for cluster, connections in cluster_connections.items():

        x_start, y_start = cluster.position.x, cluster.top_center.y
        step = cluster.width / len(connections)

        for i, connection in enumerate(connections):
            x = x_start + i * step
            y_stop = y_start + vis_params.line_base_height * (i + 1)
            draw_unary_connection(fig, vis_params, connection.label, x, y_start, y_stop)


def draw_unary_connection(
    fig: go.Figure,
    vis_params: UnaryConnectionParams,
    label: str,
    x: float,
    y_start: float,
    y_stop: float,
) -> None:
    """Draws a single unary connection using Plotly.

    Args:
        fig: Plotly Figure to draw on.
        vis_params: Visualization parameters.
        label: A label for the connection.
        x: X coordinate of the start point.
        y_start: Y coordinate of the vertical line start point.
        y_stop: Y coordinate of the vertical line end point.
    """
    fig.add_trace(
        go.Scatter(
            x=[x, x],
            y=[y_start, y_stop],
            mode="lines",
            line=dict(color=vis_params.line_color, width=vis_params.line_width),
            opacity=vis_params.line_alpha,
            showlegend=False,
        )
    )

    fig.add_annotation(
        x=x,
        y=y_stop + vis_params.label_offset,
        text=label,
        showarrow=False,
        font=dict(size=vis_params.label_fontsize, color=vis_params.label_color),
        opacity=vis_params.label_alpha,
        xanchor="center",
        yanchor="bottom",
    )


def imu_measurement(t1: int, t2: int) -> ContinuousImu[ProcessedImu]:
    """Continuous IMU measurement in range [0, 3] with 3 raw measurements."""
    data = ImuData(one_vector3, one_vector3)
    cov = ImuCovariance(i3x3, i3x3, i3x3, i3x3, i3x3)
    imus = [ProcessedImu(i, data, cov, i4x4) for i in range(3)]
    return ContinuousImu(imus, t1, t2)


def pim() -> gtsam.PreintegratedCombinedMeasurements:
    """Preintegrated IMU measurements."""
    params = gtsam.PreintegrationCombinedParams([0, 0, -9.8])
    return gtsam.PreintegratedCombinedMeasurements(params)


def create_graph1() -> Graph:
    """Test graph."""
    graph = Graph()
    t1, t2, t3, t4, t5 = 0, 1, 2, 3, 4
    p1, p2, p3 = Pose(0), Pose(1), Pose(2)
    v1, v3 = LinearVelocity(0), LinearVelocity(1)
    b1, b3 = ImuBias(0), ImuBias(1)
    noise = se3_isotropic_noise_model(1)
    m1, m2, m3 = [PoseMeasurement(t, i4x4, i3x3, i3x3) for t in [t1, t2, t3]]

    m4 = Odometry(t4, TimeRange(t1, t4), i4x4, i3x3, i3x3)
    m5 = Odometry(t5, TimeRange(t4, t5), i4x4, i3x3, i3x3)
    m6 = Odometry(t5, TimeRange(t1, t5), i4x4, i3x3, i3x3)

    m7 = imu_measurement(t1, t5)

    edge1, edge2, edge3 = (
        PriorPose(p1, m1, noise),
        PriorPose(p1, m2, noise),
        PriorPose(p1, m3, noise),
    )
    edge4, edge5, edge6 = (
        PoseOdometry(p1, p2, m4, noise),
        PoseOdometry(p2, p3, m5, noise),
        PoseOdometry(p1, p3, m6, noise),
    )

    edge7 = ImuOdometry(p1, v1, b1, p3, v3, b3, m7, pim())

    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, {p1: t1}, (NewVertex(p1, cluster1, t1),))
    element2 = GraphElement(edge2, {p1: t2})
    element3 = GraphElement(edge3, {p1: t3})
    element4 = GraphElement(edge4, {p1: t1, p2: t4}, (NewVertex(p2, cluster2, t4),))
    element5 = GraphElement(edge5, {p2: t4, p3: t5}, (NewVertex(p3, cluster3, t5),))
    element6 = GraphElement(edge6, {p1: t1, p3: t5})
    element7 = GraphElement(
        edge7,
        {p1: t1, p3: t5, v1: t1, v3: t5, b1: t1, b3: t5},
        (
            NewVertex(v1, cluster1, t1),
            NewVertex(v3, cluster3, t5),
            NewVertex(b1, cluster1, t1),
            NewVertex(b3, cluster3, t5),
        ),
    )
    graph.add_elements([element1, element2, element3, element4, element5, element6, element7])

    return graph


def create_graph2() -> Graph:
    """Test graph."""
    graph = Graph()
    t1, t2, t3, t4, t5 = 0, 1, 2, 3, 4
    p1, p2, p3 = Pose(0), Pose(1), Pose(2)
    v1, v2 = LinearVelocity(0), LinearVelocity(1)
    b1, b2 = ImuBias(0), ImuBias(1)
    noise = se3_isotropic_noise_model(1)
    m1, m2, m3 = [PoseMeasurement(t, i4x4, i3x3, i3x3) for t in [t1, t2, t3]]

    m4 = Odometry(t4, TimeRange(t1, t4), i4x4, i3x3, i3x3)
    m5 = Odometry(t5, TimeRange(t4, t5), i4x4, i3x3, i3x3)
    m6 = Odometry(t5, TimeRange(t1, t5), i4x4, i3x3, i3x3)

    m7 = imu_measurement(t1, t4)

    edge1, edge2, edge3 = (
        PriorPose(p1, m1, noise),
        PriorPose(p1, m2, noise),
        PriorPose(p1, m3, noise),
    )
    edge4, edge5, edge6 = (
        PoseOdometry(p1, p2, m4, noise),
        PoseOdometry(p2, p3, m5, noise),
        PoseOdometry(p1, p3, m6, noise),
    )

    edge7 = ImuOdometry(p1, v1, b1, p2, v2, b2, m7, pim())

    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, {p1: t1}, (NewVertex(p1, cluster1, t1),))
    element2 = GraphElement(edge2, {p1: t2})
    element3 = GraphElement(edge3, {p1: t3})
    element4 = GraphElement(edge4, {p1: t1, p2: t4}, (NewVertex(p2, cluster2, t4),))
    element5 = GraphElement(edge5, {p2: t4, p3: t5}, (NewVertex(p3, cluster3, t5),))
    element6 = GraphElement(edge6, {p1: t1, p3: t5})
    element7 = GraphElement(
        edge7,
        {p1: t1, p2: t4, v1: t1, v2: t4, b1: t1, b2: t4},
        (
            NewVertex(v1, cluster1, t1),
            NewVertex(v2, cluster2, t4),
            NewVertex(b1, cluster1, t1),
            NewVertex(b2, cluster2, t4),
        ),
    )
    graph.add_elements([element1, element2, element3, element4, element5, element6, element7])

    return graph


if __name__ == "__main__":

    graph = create_graph1()

    data = create_data(graph)

    params = VisualizationParams()
    draw(data, params)
