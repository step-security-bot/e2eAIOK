"""
 Copyright 2024 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

from .base import BaseOperation, AUTOFEOPERATORS

class TupleOperation(BaseOperation):        
    def __init__(self, op_base):
        super().__init__(op_base)
        self.support_spark_dataframe = False
        self.support_spark_rdd = True
        self.feature_in = self.op.config['src']
        self.feature_out = self.op.config['dst']

    def get_function_pd(self, trans_type = 'fit_transform'):
        feature_in = self.feature_in.copy()
        feature_out = self.feature_out
        def process(df):
            df[feature_out] = df[feature_in].apply(tuple, axis=1)
            return df
        return process

    def get_function_spark(self, rdp, trans_type = 'fit_transform'):
        raise NotImplementedError(f"CoordinatesOperation spark dataframe is not supported yet.")
AUTOFEOPERATORS.register(TupleOperation, "tuple")