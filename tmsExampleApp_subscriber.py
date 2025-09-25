
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
import math
import rti.connextdds as dds
from tmsExampleApp import tms

# class tms_DeviceInfoSubscriber:

#     @staticmethod
#     def process_data(reader):
#         # take_data() returns copies of all the data samples in the reader
#         # and removes them. To also take the SampleInfo meta-data, use take().
#         # To not remove the data from the reader, use read_data() or read().
#         samples = reader.take_data()
#         for sample in samples:
#             print(f"Received: {sample}")
    
#         return len(samples)

#     @staticmethod
#     def run_subscriber(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, 'Example tms.DeviceInfo', tms.DeviceInfo)

#         # This DataReader reads data on Topic "Example tms.DeviceInfo".
#         # DataReader QoS is configured in USER_QOS_PROFILES.xml
#         reader = dds.DataReader(participant.implicit_subscriber, topic)
#         # Initialize samples_read to zero
#         samples_read = 0

#         # Associate a handler with the status condition. This will run when the
#         # condition is triggered, in the context of the dispatch call (see below)
#         # condition argument is not used
#         def condition_handler(_):
#             nonlocal samples_read
#             nonlocal reader
#             samples_read += tms_DeviceInfoSubscriber.process_data(reader)
#         # Obtain the DataReader's Status Condition
#         status_condition = dds.StatusCondition(reader)

#         # Enable the 'data available' status and set the handler.
#         status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
#         status_condition.set_handler(condition_handler)

#         # Create a WaitSet and attach the StatusCondition
#         waitset = dds.WaitSet()
#         waitset += status_condition

#         while samples_read < sample_count:
#             # Catch control-C interrupt
#             try:
#                 # Dispatch will call the handlers associated to the WaitSet conditions
#                 # when they activate
#                 print("sleeping for 1 second...")

#                 waitset.dispatch(dds.Duration(1))  # Wait up to 1s each time
#             except KeyboardInterrupt:
#                 break

#         print('preparing to shut down...')



# class tms_PowerPortStateSubscriber:

#     @staticmethod
#     def process_data(reader):
#         # take_data() returns copies of all the data samples in the reader
#         # and removes them. To also take the SampleInfo meta-data, use take().
#         # To not remove the data from the reader, use read_data() or read().
#         samples = reader.take_data()
#         for sample in samples:
#             print(f"Received: {sample}")
    
#         return len(samples)

#     @staticmethod
#     def run_subscriber(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, 'Example tms.PowerPortState', tms.PowerPortState)

#         # This DataReader reads data on Topic "Example tms.DeviceInfo".
#         # DataReader QoS is configured in USER_QOS_PROFILES.xml
#         reader = dds.DataReader(participant.implicit_subscriber, topic)
#         # Initialize samples_read to zero
#         samples_read = 0

#         # Associate a handler with the status condition. This will run when the
#         # condition is triggered, in the context of the dispatch call (see below)
#         # condition argument is not used
#         def condition_handler(_):
#             nonlocal samples_read
#             nonlocal reader
#             samples_read += tms_PowerPortStateSubscriber.process_data(reader)
#         # Obtain the DataReader's Status Condition
#         status_condition = dds.StatusCondition(reader)

#         # Enable the 'data available' status and set the handler.
#         status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
#         status_condition.set_handler(condition_handler)

#         # Create a WaitSet and attach the StatusCondition
#         waitset = dds.WaitSet()
#         waitset += status_condition

#         while samples_read < sample_count:
#             # Catch control-C interrupt
#             try:
#                 # Dispatch will call the handlers associated to the WaitSet conditions
#                 # when they activate
#                 print("sleeping for 1 second...")

#                 waitset.dispatch(dds.Duration(1))  # Wait up to 1s each time
#             except KeyboardInterrupt:
#                 break

#         print('preparing to shut down...')


class tms_ACPowerLineMeasurementSubscriber:

    @staticmethod
    def process_data(reader):
        # take_data() returns copies of all the data samples in the reader
        # and removes them. To also take the SampleInfo meta-data, use take().
        # To not remove the data from the reader, use read_data() or read().
        received_samples = []
        samples = reader.take_data()
        for sample in samples:
            print(f"Received: {sample}")
            received_samples.append(sample)
 
        received_samples_str = str(received_samples)
        received_samples_str = received_samples_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
        received_samples_split = received_samples_str.split(',')
        numeric_values = [float(value.split('=')[-1]) for value in received_samples_split if '=' in value]
        # s = math.sqrt(numeric_values[4]**2 + numeric_values[5]**2)
        # print(s)
        
        # Still need to figure out the concept here
        if numeric_values[4] > 1:
            tms_PowerPortStatePublisher.run_publisher(domain_id=0, sample_count=2)
        
        return len(samples)



    @staticmethod
    def run_subscriber(domain_id: int, sample_count: int):

        # A DomainParticipant allows an application to begin communicating in
        # a DDS domain. Typically there is one DomainParticipant per application.
        # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
        participant = dds.DomainParticipant(domain_id)

        # A Topic has a name and a datatype.
        # topic = dds.Topic(participant, 'Example tms.ACMeasurementUpdate', tms.ac.MeasurementUpdate)
        # topic = dds.Topic(participant, 'Example tms.ACMeasurementUpdate', tms.ac.PowerLineMeasurement)
        topic = dds.Topic(participant, 'Example tms.ACPowerLineMeasurement', tms.ac.PowerLineMeasurement)
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
            samples_read += tms_ACPowerLineMeasurementSubscriber.process_data(reader)
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





class tms_PowerPortStatePublisher:

    @staticmethod
    def run_publisher(domain_id: int, sample_count: int):

        # A DomainParticipant allows an application to begin communicating in
        # a DDS domain. Typically there is one DomainParticipant per application.
        # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
        participant = dds.DomainParticipant(domain_id)

        # A Topic has a name and a datatype.
        topic = dds.Topic(participant, "Example tms.PowerPortState", tms.PowerPortState)

        # This DataWriter will write data on Topic "Example tms.DeviceInfo"
        # DataWriter QoS is configured in USER_QOS_PROFILES.xml
        writer = dds.DataWriter(participant.implicit_publisher, topic)
        sample = tms.PowerPortState("1")

        for count in range(sample_count):
            # Catch control-C interrupt
            try:
                # Modify the data to be sent here
                
                print(f"Writing tms.PowerPortState, count {count}")
                writer.write(sample)
                time.sleep(1)
            except KeyboardInterrupt:
                break

        print("preparing to shut down...")



# class tms_ACPowerLineMeasurementSequenceSubscriber:

#     @staticmethod
#     def process_data(reader):
#         # take_data() returns copies of all the data samples in the reader
#         # and removes them. To also take the SampleInfo meta-data, use take().
#         # To not remove the data from the reader, use read_data() or read().
#         samples = reader.take_data()
#         for sample in samples:
#             print(f"Received: {sample}")
    
#         return len(samples)

#     @staticmethod
#     def run_subscriber(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         # topic = dds.Topic(participant, 'Example tms.ACMeasurementUpdate', tms.ac.MeasurementUpdate)
#         # topic = dds.Topic(participant, 'Example tms.ACMeasurementUpdate', tms.ac.PowerLineMeasurement)
#         topic = dds.Topic(participant, 'Example tms.ACPowerLineMeasurementSequence', tms.ac.PowerLineMeasurementSequence)
#         # This DataReader reads data on Topic "Example tms.DeviceInfo".
#         # DataReader QoS is configured in USER_QOS_PROFILES.xml
#         reader = dds.DataReader(participant.implicit_subscriber, topic)
#         # Initialize samples_read to zero
#         samples_read = 0

#         # Associate a handler with the status condition. This will run when the
#         # condition is triggered, in the context of the dispatch call (see below)
#         # condition argument is not used
#         def condition_handler(_):
#             nonlocal samples_read
#             nonlocal reader
#             samples_read += tms_ACPowerLineMeasurementSequenceSubscriber.process_data(reader)
#         # Obtain the DataReader's Status Condition
#         status_condition = dds.StatusCondition(reader)

#         # Enable the 'data available' status and set the handler.
#         status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
#         status_condition.set_handler(condition_handler)

#         # Create a WaitSet and attach the StatusCondition
#         waitset = dds.WaitSet()
#         waitset += status_condition

#         while samples_read < sample_count:
#             # Catch control-C interrupt
#             try:
#                 # Dispatch will call the handlers associated to the WaitSet conditions
#                 # when they activate
#                 print("sleeping for 1 second...")

#                 waitset.dispatch(dds.Duration(1))  # Wait up to 1s each time
#             except KeyboardInterrupt:
#                 break

#         print('preparing to shut down...')



# class tms_PowerSwitchRequestSubscriber:

#     @staticmethod
#     def process_data(reader):
#         # take_data() returns copies of all the data samples in the reader
#         # and removes them. To also take the SampleInfo meta-data, use take().
#         # To not remove the data from the reader, use read_data() or read().
#         samples = reader.take_data()
#         for sample in samples:
#             print(f"Received: {sample}")
    
#         return len(samples)

#     @staticmethod
#     def run_subscriber(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, 'Example tms.PowerSwitchRequest', tms.PowerSwitchRequest)

#         # This DataReader reads data on Topic "Example tms.DeviceInfo".
#         # DataReader QoS is configured in USER_QOS_PROFILES.xml
#         reader = dds.DataReader(participant.implicit_subscriber, topic)
#         # Initialize samples_read to zero
#         samples_read = 0

#         # Associate a handler with the status condition. This will run when the
#         # condition is triggered, in the context of the dispatch call (see below)
#         # condition argument is not used
#         def condition_handler(_):
#             nonlocal samples_read
#             nonlocal reader
#             samples_read += tms_PowerSwitchRequestSubscriber.process_data(reader)
#         # Obtain the DataReader's Status Condition
#         status_condition = dds.StatusCondition(reader)

#         # Enable the 'data available' status and set the handler.
#         status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
#         status_condition.set_handler(condition_handler)

#         # Create a WaitSet and attach the StatusCondition
#         waitset = dds.WaitSet()
#         waitset += status_condition

#         while samples_read < sample_count:
#             # Catch control-C interrupt
#             try:
#                 # Dispatch will call the handlers associated to the WaitSet conditions
#                 # when they activate
#                 print("sleeping for 1 second...")

#                 waitset.dispatch(dds.Duration(1))  # Wait up to 1s each time
#             except KeyboardInterrupt:
#                 break

#         print('preparing to shut down...')


# class tms_ReplySubscriber:

#     @staticmethod
#     def process_data(reader):
#         # take_data() returns copies of all the data samples in the reader
#         # and removes them. To also take the SampleInfo meta-data, use take().
#         # To not remove the data from the reader, use read_data() or read().
#         samples = reader.take_data()
#         for sample in samples:
#             print(f"Received: {sample}")
    
#         return len(samples)

#     @staticmethod
#     def run_subscriber(domain_id: int, sample_count: int):

#         # A DomainParticipant allows an application to begin communicating in
#         # a DDS domain. Typically there is one DomainParticipant per application.
#         # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
#         participant = dds.DomainParticipant(domain_id)

#         # A Topic has a name and a datatype.
#         topic = dds.Topic(participant, 'Example tms.Reply', tms.Reply)

#         # This DataReader reads data on Topic "Example tms.DeviceInfo".
#         # DataReader QoS is configured in USER_QOS_PROFILES.xml
#         reader = dds.DataReader(participant.implicit_subscriber, topic)
#         # Initialize samples_read to zero
#         samples_read = 0

#         # Associate a handler with the status condition. This will run when the
#         # condition is triggered, in the context of the dispatch call (see below)
#         # condition argument is not used
#         def condition_handler(_):
#             nonlocal samples_read
#             nonlocal reader
#             samples_read += tms_ReplySubscriber.process_data(reader)
#         # Obtain the DataReader's Status Condition
#         status_condition = dds.StatusCondition(reader)

#         # Enable the 'data available' status and set the handler.
#         status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
#         status_condition.set_handler(condition_handler)

#         # Create a WaitSet and attach the StatusCondition
#         waitset = dds.WaitSet()
#         waitset += status_condition

#         while samples_read < sample_count:
#             # Catch control-C interrupt
#             try:
#                 # Dispatch will call the handlers associated to the WaitSet conditions
#                 # when they activate
#                 print("sleeping for 1 second...")

#                 waitset.dispatch(dds.Duration(1))  # Wait up to 1s each time
#             except KeyboardInterrupt:
#                 break

#         print('preparing to shut down...')



if __name__ == '__main__':
    # tms_DeviceInfoSubscriber.run_subscriber(
    #         domain_id=0,
    #         sample_count=2)
    # tms_PowerPortStateSubscriber.run_subscriber(
    #         domain_id=0,
    #         sample_count=2)
    tms_ACPowerLineMeasurementSubscriber.run_subscriber(
            domain_id=0,
            sample_count=2)
    # tms_PowerSwitchRequestSubscriber.run_subscriber(
    #         domain_id=0,
    #         sample_count=2)
    # tms_ReplySubscriber.run_subscriber(
    #         domain_id=0,
    #         sample_count=2)
