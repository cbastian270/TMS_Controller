
# (c) Copyright, Real-Time Innovations, 2022.  All rights reserved.
# RTI grants Licensee a license to use, modify, compile, and create derivative
# works of the software solely for use with RTI Connext DDS. Licensee may
# redistribute copies of the software provided that all such copies are subject
# to this license. The software is provided "as is", with no warranty of any
# type, including any warranty for fitness for any purpose. RTI is under no
# obligation to maintain or support the software. RTI shall not be liable for
# any incidental or consequential damages arising out of the use or inability
# to use the software.

import time
import sys
import rti.connextdds as dds
from tmsExampleApp import tms

# class tms_DeviceInfoPublisher:

#     @staticmethod
#     def run_publisher(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, "Example tms.DeviceInfo", tms.DeviceInfo)

#         # This DataWriter will write data on Topic "Example tms.DeviceInfo"
#         # DataWriter QoS is configured in USER_QOS_PROFILES.xml
#         writer = dds.DataWriter(participant.implicit_publisher, topic)
#         sample = tms.DeviceInfo()

# # "Type IV Distribution System", "Smart Distribution System", "SDS", "B.5, B.17, B.18", 
#         for count in range(sample_count):
#             # Catch control-C interrupt
#             try:
#                 # Modify the data to be sent here
                
#                 print(f"Writing tms.DeviceInfo, count {count}")
#                 writer.write(sample)
#                 time.sleep(1)
#             except KeyboardInterrupt:
#                 break

#         print("preparing to shut down...")


# class tms_PowerPortStatePublisher:

#     @staticmethod
#     def run_publisher(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, "Example tms.PowerPortState", tms.PowerPortState)

#         # This DataWriter will write data on Topic "Example tms.DeviceInfo"
#         # DataWriter QoS is configured in USER_QOS_PROFILES.xml
#         writer = dds.DataWriter(participant.implicit_publisher, topic)
#         sample = tms.PowerPortState()

#         for count in range(sample_count):
#             # Catch control-C interrupt
#             try:
#                 # Modify the data to be sent here
                
#                 print(f"Writing tms.PowerPortState, count {count}")
#                 writer.write(sample)
#                 time.sleep(1)
#             except KeyboardInterrupt:
#                 break

#         print("preparing to shut down...")

def pulldata(file_path):
    try:
        with open(file_path, 'r') as file:
            line = file.readline().strip()
            numbers = line.split(', ')
            numbers = [float(num) for num in numbers]
            return numbers
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("An error occurred while trying to read the acMeasurementFile", e)




class tms_PowerPortStateSubscriber:

    @staticmethod
    def process_data(reader):
        # take_data() returns copies of all the data samples in the reader
        # and removes them. To also take the SampleInfo meta-data, use take().
        # To not remove the data from the reader, use read_data() or read().
        samples = reader.take_data()
        for sample in samples:
            print(f"Received: {sample}")
    
        return len(samples)

    @staticmethod
    def run_subscriber(domain_id: int, sample_count: int):

        # A DomainParticipant allows an application to begin communicating in
        # a DDS domain. Typically there is one DomainParticipant per application.
        # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
        participant = dds.DomainParticipant(domain_id)

        # A Topic has a name and a datatype.
        topic = dds.Topic(participant, 'Example tms.PowerPortState', tms.PowerPortState)

        # This DataReader reads data on Topic "Example tms.DeviceInfo".
        # DataReader QoS is configured in USER_QOS_PROFILES.xml
        reader = dds.DataReader(participant.implicit_subscriber, topic)
        # Initialize samples_read to zero
        samples_read = 0

        # Associate a handler with the status condition. This will run when the
        # condition is triggered, in the context of the dispatch call (see below)
        # condition argument is not used
        def condition_handler(_):
            nonlocal samples_read
            nonlocal reader
            samples_read += tms_PowerPortStateSubscriber.process_data(reader)
        # Obtain the DataReader's Status Condition
        status_condition = dds.StatusCondition(reader)

        # Enable the 'data available' status and set the handler.
        status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
        status_condition.set_handler(condition_handler)

        # Create a WaitSet and attach the StatusCondition
        waitset = dds.WaitSet()
        waitset += status_condition

        while samples_read < sample_count:
            # Catch control-C interrupt
            try:
                # Dispatch will call the handlers associated to the WaitSet conditions
                # when they activate
                print("sleeping for 1 second...")

                waitset.dispatch(dds.Duration(1))  # Wait up to 1s each time
            except KeyboardInterrupt:
                break

        print('preparing to shut down...')






class tms_ACPowerLineMeasurementPublisher:

    @staticmethod
    def run_publisher(domain_id: int, sample_count: int):

        # A DomainParticipant allows an application to begin communicating in
        # a DDS domain. Typically there is one DomainParticipant per application.
        # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
        participant = dds.DomainParticipant(domain_id)

        # A Topic has a name and a datatype.
        topic = dds.Topic(participant, "Example tms.ACPowerLineMeasurement", tms.ac.PowerLineMeasurement)
        # topic = dds.Topic(participant, "Example tms.ACMeasurementUpdate", tms.ac.MeasurementUpdate)
        # This DataWriter will write data on Topic "Example tms.DeviceInfo"
        # DataWriter QoS is configured in USER_QOS_PROFILES.xml
        writer = dds.DataWriter(participant.implicit_publisher, topic)
        inputData = pulldata("4RTI.txt")
        
        sample = tms.ac.PowerLineMeasurement(*inputData)
        for count in range(sample_count):
            # Catch control-C interrupt
            try:
                # Modify the data to be sent here
                
                print(f"Writing tms.ACPowerLineMeasurement, count {count}")
                writer.write(sample)
                time.sleep(1)
            except KeyboardInterrupt:
                break

        print("preparing to shut down...")

# # ACMeasurementUpdate for Line2
# class tms_ACPowerLineMeasurementPublisher2:

#     @staticmethod
#     def run_publisher(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, "Example tms.ACPowerLineMeasurement", tms.ac.PowerLineMeasurement)
#         # topic = dds.Topic(participant, "Example tms.ACMeasurementUpdate", tms.ac.MeasurementUpdate)
#         # This DataWriter will write data on Topic "Example tms.DeviceInfo"
#         # DataWriter QoS is configured in USER_QOS_PROFILES.xml
#         writer = dds.DataWriter(participant.implicit_publisher, topic)
#         inputData = pulldata("testDataFile2")
        
#         sample = tms.ac.PowerLineMeasurement(*inputData)
#         for count in range(sample_count):
#             # Catch control-C interrupt
#             try:
#                 # Modify the data to be sent here
                
#                 print(f"Writing tms.ACMeasurementUpdate2, count {count}")
#                 writer.write(sample)
#                 time.sleep(1)
#             except KeyboardInterrupt:
#                 break

#         print("preparing to shut down...")


# # ACMeasurementUpdate for Line 3
# class tms_ACPowerLineMeasurementPublisher3:

#     @staticmethod
#     def run_publisher(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, "Example tms.ACPowerLineMeasurement", tms.ac.PowerLineMeasurement)
#         # topic = dds.Topic(participant, "Example tms.ACMeasurementUpdate", tms.ac.MeasurementUpdate)
#         # This DataWriter will write data on Topic "Example tms.DeviceInfo"
#         # DataWriter QoS is configured in USER_QOS_PROFILES.xml
#         writer = dds.DataWriter(participant.implicit_publisher, topic)
#         inputData = pulldata("testDataFile3")
        
#         sample = tms.ac.PowerLineMeasurement(*inputData)
#         for count in range(sample_count):
#             # Catch control-C interrupt
#             try:
#                 # Modify the data to be sent here
                
#                 print(f"Writing tms.ACMeasurementUpdate3, count {count}")
#                 writer.write(sample)
#                 time.sleep(1)
#             except KeyboardInterrupt:
#                 break

#         print("preparing to shut down...")


# class tms_ACPowerLineMeasurementSequencePublisher:

#     @staticmethod
#     def run_publisher(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, "Example tms.ACPowerLineMeasurementSequence", tms.ac.PowerLineMeasurementSequence)
#         # topic = dds.Topic(participant, "Example tms.ACMeasurementUpdate", tms.ac.MeasurementUpdate)
#         # This DataWriter will write data on Topic "Example tms.DeviceInfo"
#         # DataWriter QoS is configured in USER_QOS_PROFILES.xml
#         writer = dds.DataWriter(participant.implicit_publisher, topic)
#         inputData = pulldata("testDataFile3")
        
#         sample = tms.ac.PowerLineMeasurementSequence(inputData)
#         for count in range(sample_count):
#             # Catch control-C interrupt
#             try:
#                 # Modify the data to be sent here
                
#                 print(f"Writing tms.ACPowerLineMeasurementSequence, count {count}")
#                 writer.write(sample)
#                 time.sleep(1)
#             except KeyboardInterrupt:
#                 break

#         print("preparing to shut down...")


# class tms_PowerSwitchRequestPublisher:

#     @staticmethod
#     def run_publisher(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, "Example tms.PowerSwitchRequest", tms.PowerSwitchRequest)

#         # This DataWriter will write data on Topic "Example tms.DeviceInfo"
#         # DataWriter QoS is configured in USER_QOS_PROFILES.xml
#         writer = dds.DataWriter(participant.implicit_publisher, topic)
#         sample = tms.PowerSwitchRequest()

#         for count in range(sample_count):
#             # Catch control-C interrupt
#             try:
#                 # Modify the data to be sent here
                
#                 print(f"Writing tms.PowerSwitchRequest, count {count}")
#                 writer.write(sample)
#                 time.sleep(1)
#             except KeyboardInterrupt:
#                 break

#         print("preparing to shut down...")


# class tms_ReplyPublisher:

#     @staticmethod
#     def run_publisher(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, "Example tms.Reply", tms.Reply)

#         # This DataWriter will write data on Topic "Example tms.DeviceInfo"
#         # DataWriter QoS is configured in USER_QOS_PROFILES.xml
#         writer = dds.DataWriter(participant.implicit_publisher, topic)
#         sample = tms.Reply()

#         for count in range(sample_count):
#             # Catch control-C interrupt
#             try:
#                 # Modify the data to be sent here
                
#                 print(f"Writing tms.Reply, count {count}")
#                 writer.write(sample)
#                 time.sleep(1)
#             except KeyboardInterrupt:
#                 break

#         print("preparing to shut down...")




if __name__ == '__main__':
    # tms_DeviceInfoPublisher.run_publisher(
    #         domain_id=0,
    #         sample_count=2)
    # tms_PowerPortStatePublisher.run_publisher(
    #         domain_id=0,
    #         sample_count=2)
    tms_ACPowerLineMeasurementPublisher.run_publisher(
        domain_id=0,
        sample_count=2)

    tms_PowerPortStateSubscriber.run_subscriber(
            domain_id=0,
            sample_count=2)
    # tms_PowerSwitchRequestPublisher.run_publisher(
    #     domain_id=0,
    #     sample_count=2)    
    # tms_ReplyPublisher.run_publisher(
    #     domain_id=0,
    #     sample_count=2)