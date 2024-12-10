class Segment:
    def __init__(self, title, uniqueId, sources=None):
        self.title = title
        self.uniqueId = uniqueId
        self.sources = sources or {}

    def _serialize_sub_stories(self, depth):
        """Helper function to serialize sources with depth control.

        Args:
            depth (int): Maximum depth for serializing nested segments

        Returns:
            dict: Serialized sources dictionary
        """
        serialized = {}
        for key, sources_list in self.sources.items():
            serialized_sources = []
            for source in sources_list:
                if hasattr(source, "__json__") and not isinstance(source, dict):
                    serialized_sources.append(source.__json__(depth - 1))
                else:
                    serialized_sources.append(source)
            serialized[key] = serialized_sources
        return serialized

    def __json__(self, depth=10):
        """Make the class directly JSON serializable

        Args:
            depth (int): Maximum depth for serializing nested sources. Defaults to 10.
        """
        if depth <= 0:  # Base case to prevent infinite recursion
            return {
                "title": self.title,
                "uniqueId": self.uniqueId,
                "sources": {},
            }

        return {
            "title": self.title,
            "uniqueId": self.uniqueId,
            "sources": self._serialize_sub_stories(depth),
        }

    @classmethod
    def from_dict(cls, publication_dict):
        """Factory method to create a Publication from a dictionary"""
        publication = cls(
            title=publication_dict.get("title", ""),
            uniqueId=publication_dict.get("uniqueId", ""),
            sources=publication_dict.get("sources", {}),
        )

        # Set any additional attributes
        for key, value in publication_dict.items():
            if not hasattr(publication, key) and key != "sources":  # Skip sources as we've already handled it
                setattr(publication, key, value)

        return publication

    def getCombinedSubStoryContext(self):
        """Get combined context from all sources"""
        contexts = [self.title]
        for sources_list in self.sources.values():
            for source in sources_list:
                if hasattr(source, "getStoryContext"):
                    contexts.append(source.getStoryContext())
                elif isinstance(source, str):
                    contexts.append(source)
        return "\n".join(contexts)

    def to_dict(self):
        """Convert the Publication instance to a dictionary"""
        return self.__dict__.copy()
