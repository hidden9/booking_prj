from time import time, sleep

class ThrottleBackendBase:
    def incr_bucket(self, zone_name, bucket_key, bucket_num, bucket_num_next, bucket_span, cost=1):
        """
        Increments the limit for the given bucket.
        @returns: the new value of the bucket, post-increment
        """
        raise NotImplementedError



class SlidingWindow:

    def __init__(self, capacity, time_unit, forward_callback, drop_callback):
        self.capacity = capacity
        self.time_unit = time_unit
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback

        self.cur_time = time()
        self.pre_count = capacity
        self.cur_count = 0

    

    def handle(self, packet):

        if (time() - self.cur_time) > self.time_unit:
            self.cur_time = time()
            self.pre_count = self.cur_count
            self.cur_count = 0

        ec = (self.pre_count * (self.time_unit - (time() - self.cur_time)) / self.time_unit) + self.cur_count

        if (ec > self.capacity):
            return self.drop_callback(packet)

        self.cur_count += 1
        return self.forward_callback(packet)