class IssueFormatter:
    """Converts a cppcheck error into a codeclimate issue."""

    def __init__(self, node, misra_blockers):
        self.node = node
        self.misra_blockers = misra_blockers

    def format(self):
        if len(self.node) == 0:
            # No location for this issue: likely to be a general information issue,
            # should be safe to ignore.
            return None

        issue = {}
        issue['type'] = 'issue'
        issue['check_name'] = self.node.get('id')

        issue['content'] = {}
        issue['content']['body'] = self.node.get('verbose').replace("'", "`")
        if self.node.get('cwe'):
            # Include CWE link for detailed information.
            issue['content']['body'] += (
                ' ([detailed CWE explanation](https://cwe.mitre.org/data/'
                'definitions/{}.html))'.format(self.node.get('cwe')))

        issue['description'] = '[{}] '.format(self.node.get('id'))
        issue['description'] += issue['content']['body']

        has_violation = False
        if issue['check_name'] in self.misra_blockers:
            has_violation = True

        category, issue['severity'] = (
            self._derive_category_and_severity(self.node.get('severity'), has_violation))
        issue['categories'] = [category]

        issue['location'] = self._convert_location(self.node[0])
        issue['other_locations'] = []
        if len(self.node) > 1:
            locations = list(self.node)[1:]
            for l in locations:
                if l.get('line') is not None:
                    location = self._convert_location(l)
                    issue['other_locations'].append(location)

        return issue

    def _convert_location(self, location):
        """Converts cppcheck error location to the format codeclimate requires."""
        path = location.get('file')
        line = location.get('line')

        location = {}
        location['path'] = path
        location['lines'] = {}
        location['lines']['begin'] = int(line)
        location['lines']['end'] = int(line)

        return location

    def _derive_category_and_severity(self, severity, violation):
        """Derives codeclimate issue category & severity from cppcheck severity."""
        # http://cppcheck.sourceforge.net/devinfo/doxyoutput/classSeverity.html
        # https://github.com/codeclimate/spec/blob/master/SPEC.md
        if violation or severity == 'error':
            return ('Performance', 'blocker')
        if severity == 'warning':
            return ('Bug Risk', 'critical')
        if severity == 'style':
            return ('Style', 'minor')
        if severity == 'performance':
            return ('Performance', 'minor')
        if severity == 'portability':
            return ('Compatibility', 'minor')
        if severity == 'none' or severity == 'information' or severity == 'debug':
            return ('Clarity', 'info')
