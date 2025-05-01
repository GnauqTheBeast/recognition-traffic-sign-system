# from sqlalchemy.orm import Session
# from models.sample import Sample
# from typing import List, Optional

# class SampleRepository:
#     def __init__(self, db: Session):
#         self.db = db
    
#     def get_all(self) -> List[Sample]:
#         return self.db.query(Sample).all()
    
#     def get_by_id(self, sample_id: int) -> Optional[Sample]:
#         return self.db.query(Sample).filter(Sample.id == sample_id).first()
    
#     def create(self, sample_data: dict) -> Sample:
#         sample = Sample(**sample_data)
#         self.db.add(sample)
#         self.db.commit()
#         self.db.refresh(sample)
#         return sample
    
#     def update(self, sample_id: int, sample_data: dict) -> Optional[Sample]:
#         sample = self.get_by_id(sample_id)
#         if sample:
#             for key, value in sample_data.items():
#                 setattr(sample, key, value)
#             self.db.commit()
#             self.db.refresh(sample)
#         return sample
    
#     def delete(self, sample_id: int) -> bool:
#         sample = self.get_by_id(sample_id)
#         if sample:
#             self.db.delete(sample)
#             self.db.commit()
#             return True
#         return False
    
#     def add_traffic_sign(self, sample_id: int, traffic_sign_id: int) -> bool:
#         """Thêm liên kết giữa Sample và TrafficSign"""
#         sample = self.get_by_id(sample_id)
#         traffic_sign = self.db.query(TrafficSign).filter(TrafficSign.id == traffic_sign_id).first()
        
#         if sample and traffic_sign:
#             sample.traffic_signs.append(traffic_sign)
#             self.db.commit()
#             return True
#         return False
    
#     def get_traffic_signs(self, sample_id: int) -> List[TrafficSign]:
#         """Lấy tất cả các biển báo liên quan đến một mẫu"""
#         sample = self.get_by_id(sample_id)
#         if sample:
#             return sample.traffic_signs
#         return []
