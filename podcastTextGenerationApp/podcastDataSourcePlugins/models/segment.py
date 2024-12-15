import yaml
from typing import List


class FollowUp:
    def __init__(self, source, question, answer):
        self.source = source
        self.question = question
        self.answer = answer

    def __json__(self):
        return {"source": self.source, "question": self.question, "answer": self.answer}

    @classmethod
    def from_dict(cls, d):
        return cls(source=d.get("source"), question=d.get("question"), answer=d.get("answer"))


class Segment:
    def __init__(self, title, uniqueId, sources=None, followUps=None):
        self.title = title
        self.uniqueId = uniqueId
        self.sources = sources or {}
        self.followUps: List[FollowUp] = followUps or []

    def _serialize_sub_stories(self, depth):
        serialized = {}
        for key, sources_list in self.sources.items():
            serialized_sources = []
            for source in sources_list:
                if hasattr(source, "__json__") and not isinstance(source, dict):
                    val = source.__json__(depth - 1)
                    if not isinstance(val, (dict, list, str, int, float, bool, type(None))):
                        val = str(val)
                    serialized_sources.append(val)
                else:
                    if not isinstance(source, (dict, list, str, int, float, bool, type(None))):
                        source = str(source)
                    serialized_sources.append(source)
            serialized[key] = serialized_sources
        return serialized

    def __json__(self, depth=10):
        if depth <= 0:
            return {"title": self.title, "uniqueId": self.uniqueId, "sources": {}, "followUps": [f.__json__() for f in self.followUps]}

        return {"title": self.title, "uniqueId": self.uniqueId, "sources": self._serialize_sub_stories(depth), "followUps": [f.__json__() for f in self.followUps]}

    @classmethod
    def from_dict(cls, publication_dict):
        followUps_data = publication_dict.get("followUps", [])
        followUps = [FollowUp.from_dict(fu) for fu in followUps_data]
        publication = cls(title=publication_dict.get("title", ""), uniqueId=publication_dict.get("uniqueId", ""), sources=publication_dict.get("sources", {}), followUps=followUps)
        for key, value in publication_dict.items():
            if not hasattr(publication, key) and key not in ("sources", "followUps"):
                setattr(publication, key, value)
        return publication

    def to_dict(self):
        return self.__json__(depth=10)

    def getCombinedSubStoryContext(self):
        contexts = [self.title]
        for sources_list in self.sources.values():
            for source in sources_list:
                if hasattr(source, "getStoryContext"):
                    contexts.append(source.getStoryContext())
                elif isinstance(source, str):
                    contexts.append(source)
        return "\n".join(contexts)

    def joinAllSources(self, limit=1):
        if not self.sources:
            return ""
        allTexts = []
        for sourcesList in self.sources.values():
            limitedSources = sourcesList[:limit]
            for source in limitedSources:
                if hasattr(source, "content"):
                    allTexts.append(source.content)
        return "\n".join(allTexts)


def segment_representer(dumper, data):
    return dumper.represent_data(data.to_dict())


# Register representers with SafeDumper since safe_dump uses SafeDumper
yaml.SafeDumper.add_representer(Segment, segment_representer)

# FollowUp objects are always converted to dicts via __json__(), so no direct representer needed.
