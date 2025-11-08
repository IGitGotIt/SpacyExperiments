"""
Name generator module for creating blended character names.
"""

import random


class NameGenerator:
    """Generates unique blended names from mythology and robot characters."""

    def __init__(self, database):
        """
        Initialize the name generator.

        Args:
            database: CharacterDatabase instance
        """
        self.db = database

    def generate(self, query=None, num_samples=100, top_n=5):
        """
        Generate unique blended names.

        Args:
            query: Optional query to guide name generation
            num_samples: Number of character pairs to sample
            top_n: Number of top results to return

        Returns:
            List of dictionaries containing blended names and metadata
        """
        # Get characters
        mythology_chars = self.db.get_random_characters(category="mythology", limit=num_samples)
        robot_chars = self.db.get_random_characters(category="robot", limit=num_samples)

        random.shuffle(mythology_chars)
        random.shuffle(robot_chars)

        # Generate blends
        all_blends = []
        for i in range(min(len(mythology_chars), len(robot_chars))):
            myth_name = mythology_chars[i]['name']
            robot_name = robot_chars[i]['name']

            if len(myth_name) < 3 or len(robot_name) < 3:
                continue
            if len(myth_name) > 20 or len(robot_name) > 20:
                continue

            blends = self._blend_names(myth_name, robot_name)

            for blend in blends:
                if self._is_pronounceable(blend):
                    all_blends.append({
                        'name': blend.capitalize(),
                        'source_myth': myth_name,
                        'source_robot': robot_name
                    })

        # Remove duplicates
        unique_blends = {}
        for blend in all_blends:
            unique_blends[blend['name']] = blend

        # Score and filter
        scored_blends = []
        for blend in unique_blends.values():
            creativity_score = self._score_creativity(
                blend['name'],
                blend['source_myth'],
                blend['source_robot']
            )

            semantic_matches = self.db.search(blend['name'], n_results=3)

            scored_blends.append({
                **blend,
                'creativity_score': creativity_score,
                'semantic_matches': semantic_matches
            })

        # If query provided, filter by relevant characters
        if query:
            query_results = self.db.search(query, n_results=10)
            relevant_chars = {r['name'] for r in query_results}

            for blend in scored_blends:
                if blend['source_myth'] in relevant_chars or blend['source_robot'] in relevant_chars:
                    blend['query_match'] = True

            scored_blends.sort(key=lambda x: (x.get('query_match', False), x['creativity_score']), reverse=True)
        else:
            scored_blends.sort(key=lambda x: x['creativity_score'], reverse=True)

        return scored_blends[:top_n]

    def _blend_names(self, myth_name, robot_name):
        """Create different blends of two names."""
        blends = []

        # Method 1: First half of myth + second half of robot
        if len(myth_name) > 2 and len(robot_name) > 2:
            mid1 = len(myth_name) // 2
            mid2 = len(robot_name) // 2
            blend1 = myth_name[:mid1] + robot_name[mid2:].lower()
            blends.append(blend1)

        # Method 2: First half of robot + second half of myth
        if len(robot_name) > 2 and len(myth_name) > 2:
            mid1 = len(robot_name) // 2
            mid2 = len(myth_name) // 2
            blend2 = robot_name[:mid1] + myth_name[mid2:].lower()
            blends.append(blend2)

        # Method 3: First 2/3 of myth + last 1/3 of robot
        if len(myth_name) > 3 and len(robot_name) > 3:
            cut1 = (len(myth_name) * 2) // 3
            cut2 = (len(robot_name) * 2) // 3
            blend3 = myth_name[:cut1] + robot_name[cut2:].lower()
            blends.append(blend3)

        # Method 4: Prefix from one, suffix from other
        if len(myth_name) > 3 and len(robot_name) > 3:
            blend4 = myth_name[:3] + robot_name[-4:].lower()
            blends.append(blend4)

        return blends

    def _is_pronounceable(self, word):
        """Check if a word is reasonably pronounceable."""
        word = word.lower()

        if len(word) < 6 or len(word) > 15:
            return False

        vowels = set('aeiouy')
        consonant_streak = 0
        vowel_streak = 0

        for char in word:
            if char in vowels:
                vowel_streak += 1
                consonant_streak = 0
                if vowel_streak > 3:
                    return False
            else:
                consonant_streak += 1
                vowel_streak = 0
                if consonant_streak > 3:
                    return False

        vowel_count = sum(1 for c in word if c in vowels)
        if vowel_count < 2:
            return False

        weird_combos = ['xz', 'qx', 'zx', 'qz', 'xq', 'xxx', 'zzz']
        for combo in weird_combos:
            if combo in word:
                return False

        return True

    def _score_creativity(self, blend_name, source_myth, source_robot):
        """Score how creative/unique a blend is."""
        score = 0

        score += len(blend_name) * 0.5

        vowels = sum(1 for c in blend_name.lower() if c in 'aeiouy')
        ratio = vowels / len(blend_name)
        if 0.3 < ratio < 0.5:
            score += 5

        myth_overlap = sum(1 for i in range(len(source_myth)-1)
                          if source_myth[i:i+2].lower() in blend_name.lower())
        robot_overlap = sum(1 for i in range(len(source_robot)-1)
                           if source_robot[i:i+2].lower() in blend_name.lower())
        score += (myth_overlap + robot_overlap) * 2

        return score
