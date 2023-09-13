import threading


# 单例基类
class Singleton:
    _thread_lock = threading.Lock()
    _instance = None

    @classmethod
    def instance(cls):
        # 如果该类有实例化对象则不再实例，直接返回之前的对象
        if cls._instance is not None:
            return cls._instance
        with cls._thread_lock:
            # 拿到线程锁还是要再判断，避免上一个线程实例化了对象
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance
