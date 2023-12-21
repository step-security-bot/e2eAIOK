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

from .base_api import base_api

class download(base_api):
    def __init__(self, name, url, unzip = False):
        super().__init__()      
        self.saved_path = self.download_url(name, url, unzip = unzip)
        print(f"Data is downloaded, use {self.saved_path} to open")
         