import json
from typing import Optional


class AssetIndex:
    def __init__(self, indices: list[str], version: float):
        self.indices = indices
        self.version = version


class MessagingMetadata:
    def __init__(self, file_path: str, metadata_path: str, version: float):
        self.version = version
        self.metadata_path = metadata_path
        self.file_path = file_path


class IndivMediaComponent:
    def __init__(self, metadata: Optional[MessagingMetadata], buffers: Optional[bytearray], file_extension: str,
                 mim_type: str, key: str, date: str, tags: AssetIndex):
        self.date = date
        self.key = key
        self.file_extension = file_extension
        self.buffers = buffers
        self.metadata = metadata
        self.mime_type = mim_type
        self.index = tags

    def set_tags(self, tags: list[str]):
        self.index.indices.extend(tags)


class MediaComponent:
    def __init__(self, values: list[IndivMediaComponent], date: int, id: str, index: AssetIndex):
        self.index = index
        self.id = id
        self.date = date
        self.values = values


def get_key(key: str, loaded) -> Optional:
    if key in loaded.keys():
        return loaded[key]


def get_key_in(key: list[str], loaded) -> Optional:
    out = None
    for key_item in key:
        out = get_key(key_item, loaded if not out else out)
    return out


class ReflectableComponent:
    def __init__(self, components: dict[str, list[MediaComponent]], id: str, symbol: str):
        self.id = id
        self.symbol = symbol
        self.components = components


def serialize_media_component(message: str) -> ReflectableComponent:
    message = json.loads(message)
    id = get_key_in(['data', 'WebData', 'inner', 'uniqueId'], message)
    value = get_key_in(['data', 'WebData', 'inner', 'data'], message)
    media_components = {}
    for key, items in value.items():
        media_components[key] = []
        for item in items:
            date = get_key('date', item)
            media_component_index = get_key('index', item)
            media_component_indices = get_key('index', media_component_index)
            media_component_version = get_key('version', media_component_index)
            values = get_key('values', item)
            indiv = []
            for value in values:
                ext = get_key('fileExtension', value)
                mime_type = get_key('mimeType', value)
                metadata = get_key('metadata', value)
                index = get_key('index', value)
                indices = get_key('index', index)
                index_version = get_key('version', index)
                buffer = get_key('buffers', value)
                if metadata:
                    file_path = get_key('filePath', metadata)
                    metadata_path = get_key('metadataPath', metadata)
                    version = get_key('version', metadata)
                    metadata = MessagingMetadata(file_path, metadata_path, version)
                    indiv.append(IndivMediaComponent(metadata, buffer, ext, mime_type, key, date, AssetIndex(indices, index_version)))
                elif buffer:
                    indiv.append(IndivMediaComponent(metadata, buffer, ext, mime_type, key, date, AssetIndex(indices, index_version)))

            media_components[key].append(MediaComponent(indiv, date, id, AssetIndex(media_component_indices, media_component_version)))

    return ReflectableComponent(media_components, id, id)


def deserialize_metadata(metadata: MessagingMetadata):
    return {
        "filePath": metadata.file_path,
        "metadataPath": metadata.metadata_path,
        "version": metadata.version
    } if metadata else None


def deserialize_index(index):
    return {
        "index": index.indices,
        "version": index.version
    }


def deserialize_media_component_indiv(indivs: dict[str, list[MediaComponent]]):
    return {
        key: [
            {
                "className": "com.hayden.reflectable.media.MediaData$WebMediaDataIndiv",
                "enumClzz": "com.hayden.shared.models.data.WebData",
                "values": [
                    {
                        "buffers": indiv.buffers,
                        "metadata": deserialize_metadata(indiv.metadata),
                        "fileExtension": indiv.file_extension,
                        "mimeType": indiv.mime_type,
                        "index": deserialize_index(indiv.index)
                    }
                    for indiv in media_component.values],
                "date": media_component.date,
                "index": deserialize_index(media_component.index)
            }
            for media_component in value] for key, value in indivs.items()
    }


def deserialize_media_component(message: ReflectableComponent) -> str:
    return json.dumps({
        "className": "com.hayden.shared.models.reflectable.ReflectableComponent",
        "data": {
            "WebData": {
                "className": "com.hayden.shared.models.reflectable.ReflectableWrapper",
                "inner": {
                    "className": "com.hayden.reflectable.media.MediaData",
                    "clzz": "com.hayden.asset.models.asset.MultiModalMediaFeed",
                    "symbol": message.id,
                    "enumClzz": "com.hayden.shared.models.data.WebData",
                    "reflectableClzz": "com.hayden.reflectable.media.MediaData$WebMediaDataIndiv",
                    "uniqueId": message.id,
                    "data": deserialize_media_component_indiv(message.components)
                },
                "type": "com.hayden.reflectable.media.ReflectableMediaItem"
            }
        }
    })
