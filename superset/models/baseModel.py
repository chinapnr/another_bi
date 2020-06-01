import datetime

from superset import db


class BaseModel:
    DB_ERROR = "DB Error: {error}"

    """
    ********************* 通用查询方法 *********************
    """

    @classmethod
    def row_to_dict(cls, row):
        """
        数据转换为字典
        :param row:
        :return:
        """
        d = {}

        if row is None:
            return None

        for column in row.__table__.columns:
            # 时间类型格式化
            if column.type.python_type == datetime.datetime:
                column_value = getattr(row, column.name)
                if column_value:
                    d[column.name] = column_value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                d[column.name] = getattr(row, column.name)
        return d

    @classmethod
    def get_condition_data_count(cls, condition):
        """
        获取符合条件的数据的条数
        :param condition:
        :return:
        """
        try:
            rows = db.session.query(cls).filter_by(**condition).count()
        except Exception as e:
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        return rows

    @classmethod
    def get_all_data(cls) -> list:
        """
        获取所有数据
        :return:
        """
        try:
            rows = db.session.query(cls).all()
        except Exception as e:
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        return [BaseModel.row_to_dict(row) for row in rows]

    @classmethod
    def get_data_by_id(cls, idd: int) -> list:
        """
        根据 ID 查询数据
        :param idd:
        :return:
        """
        try:
            rows = db.session.query(cls).filter_by(**{"id": idd}).all()
        except Exception as e:
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        return [BaseModel.row_to_dict(row) for row in rows]

    @classmethod
    def get_data_by_field(cls, field_name: str, field_value: str or int) -> list:
        """
        根据某字段查询数据
        :param field_name:
        :param field_value:
        :return:
        """
        try:
            rows = db.session.query(cls).filter_by(**{field_name: field_value}).all()
        except Exception as e:
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        return [BaseModel.row_to_dict(row) for row in rows]

    @classmethod
    def get_data_by_multiple_condition(cls, condition):
        """
        自定义多条件查询
        :param condition:
        :return:
        """
        try:
            rows = db.session.query(cls).filter_by(**condition).all()
        except Exception as e:
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        return [BaseModel.row_to_dict(row) for row in rows]

    """
    ********************* 通用新增方法 *********************
    """

    @classmethod
    def add_data(cls, data: dict) -> int:
        """
        新增数据，返回新增 ID
        :param data:
        :return:
        """
        try:
            runtime_object = cls(**data)
            db.session.add(runtime_object)
            # flush 后才能获取到本次新增的 id
            db.session.flush()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        finally:
            pass
        return runtime_object.__getattribute__("id")

    @classmethod
    def add_multiple_data(cls, data_list) -> [int]:
        """
        新增多组数据
        :param data_list:
        :return:
        """

        try:
            instance_list = []
            for data in data_list:
                runtime_object = cls(**data)
                instance_list.append(runtime_object)

            db.session.add_all(instance_list)
            # flush 后才能获取到本次新增的 id
            db.session.flush()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        finally:
            pass
        return [x.__getattribute__("id") for x in instance_list]

    """
    ********************* 通用新增方法 *********************
    """

    @classmethod
    def update_data(cls, condition: dict, data: dict) -> int:
        """
        更新数据，返回影响条数
        :param condition:
        :param data:
        :return:
        """

        try:
            rows = db.session.query(cls).filter_by(**condition).update(data)
            db.session.commit()
            return rows
        except Exception as e:
            db.session.rollback()
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        finally:
            pass

    """
    ********************* 通用删除方法 *********************
    """

    @classmethod
    def delete_data_by_id(cls, idd) -> int:
        """
        根据 id 删除数据
        :param idd:
        :return:
        """

        try:
            rows = db.session.query(cls).filter_by(**{"id": idd}).delete()
            db.session.commit()
            return rows
        except Exception as e:
            db.session.rollback()
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        finally:
            pass

    @classmethod
    def delete_data(cls, condition: dict) -> int:
        """
        删除数据
        :param condition:
        :return:
        """

        try:
            rows = db.session.query(cls).filter_by(**condition).delete()
            db.session.commit()
            return rows
        except Exception as e:
            db.session.rollback()
            raise Exception(BaseModel.DB_ERROR.format(error=e))
        finally:
            pass
