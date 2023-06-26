from rosbags.rosbag1 import Reader as RosBagReader
from rosbags.serde import deserialize_cdr, ros1_to_cdr


class Ros1BagReader(DataReader):
    def __init__():
        super().__init__()

    def get_elements(self, file_path: Path):
        pass

# def read(self, file_path, topics, batch_size=None):
    #     self.__check_file()
    #     size = 0
    #     current_message_idx = 0
    #     with RosBagReader(file_path) as reader:
    #         connections = [x for x in reader.connections if x.topic in topics]
    #         print('bag duration: ', (reader.end_time-reader.start_time)*1e-9, 'sec.')
    #         print('messages num:', reader.message_count)
    #         print('indexes num:', len(reader.indexes))
    #         print('connections num:', len(reader.connections))
    #         print('chunks num: ', len(reader.chunks))
    #         print('topics num: ', len(reader.topics))
    #         print(reader.current_chunk)
    #         prev_t = reader.start_time
    #         with open('data_config.json') as json_file:
    #             data = json.load(json_file)
    #         for i, message in enumerate(reader.messages(connections=connections)):
    #             connection, timestamp, rawdata = message
    #             data["time"].append(timestamp)
    #             data["id"].append(i)
    #             if prev_t == timestamp
    #         print(pd.DataFrame.from_dict(data, orient='columns').set_index("id"))
        #     if(t == prev_t):
        #         print('True')
        #     prev_t = t
        # for con in connections:
        # for message in reader.messages(connections=[con]):
        #         connection, timestamp, rawdata = message
        #         msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #         print(reader.read_chunk())
        # print(msg.header.frame_id)

        # dataFrames = [pd.DataFrame()]*len(generators)
        #     for gen in generators:
        #         for connection, timestamp, rawdata in gen:
        #             msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #             print(msg.header.frame_id)
        #         # for message in gen:
        #         #     connection, timestamp, rawdata = message
        #         #     msg = deserialize_cdr(ros1_to_cdr(rawdata, connections.msgtype), connections.msgtype)
        #
        #     # connection, timestamp, rawdata = next(gen)
        #     # msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #     # tmp.append(msg)
        #     start_mem = psutil.Process().memory_info().rss / (1024**2)
        #     # print(type(msg.orientation))
        #     for i, message in enumerate(gen):
        #         connection, timestamp, rawdata = message
        #         msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #         tmp.append(msg)
        #         current_RAM_used = psutil.Process().memory_info().rss / (1024 ** 2) - start_mem
        #         # print(current_RAM_used)
        #         if current_RAM_used >= batch_size:
        #             print('!!!!!!', current_RAM_used)
        #             break
        # print('sum= ',start_mem + current_RAM_used)
        # print('total= ',psutil.Process().memory_info().rss / (1024 ** 2))
        #     print(i)
        # while current_message_idx <  reader.message_count or size < batch_size:

        # topic and msgtype information is available on .connections list
        # imu_connections = [x for x in reader.connections if x.topic == '/sensors/imu_driver/imu']
        # gen = reader.messages(connections=imu_connections)
        # for message in gen:
        #     connection, timestamp, rawdata = message
        #     msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #     print(msg.angular_velocity.x)
        # msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        # print(msg.angular_velocity.x)
        # print(msg.header.frame_id)
        #
        # for connection in reader.connections:
        #     print(connection.topic, connection.msgtype)
        #
        # # iterate over messages
        # for connection, timestamp, rawdata in reader.messages():
        #     if connection.topic == '/sensors/imu_driver/imu':
        #         msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #         print(msg.header.frame_id)
        #
        # # messages() accepts connection filters
        # connections = [x for x in reader.connections if x.topic == '/sensors/imu_driver/imu']
        # for connection, timestamp, rawdata in reader.messages(connections=connections):
        #     msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #     print(msg.header.frame_id)
