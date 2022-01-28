#!/usr/bin/env python3
"""An example plugin for BoxHead.

It has to be a descendant of `boxhead.plugin.Plugin` and thus becomes a
descendant of `multiprocessing.Process`.
"""

from boxhead import config as boxhead_config
from boxhead import plugin
from boxhead.boxheadlogging import boxheadlogging

logger: boxheadlogging.BoxHeadLogger = boxheadlogging.get_logger(__name__)


class Example(plugin.Plugin):
    """The main class of the plugin.

    Needs to inherit from `boxhead.plugin.Plugin` and thus becomes a
    descendant of `multiprocessing.Process` which will be started by
    the main process some time after `on_init` is called.
    """

    def on_init(self, config: boxhead_config.Config) -> None:
        """This gets called by the constructor.

        Use this function to retrieve and store values from the
        configuration. Be careful not to store references as those
        might lead to all sorts of problems related to multiprocessing.

        Using any function but `config.get` will make sure you get
        passed a value (including copies of dictionaries / lists).

        Use this function to register for events, e.g.:
        * `register_for('specialevent')` makes sure `on_specialevent`
          gets called everytime `specialevent` is emitted by the main
          process

        You may set after which interval `on_tick` is called by setting
        the appropriate value of `_tick_interval` [s].

        Args:
            config: The configuration.
        """
        logger.debug('Hey there!')

        self._smile: str = ':)'
        #self._smile: str = config.get_str('plugins',
        #                             'example',
        #                             'smile',
        #                             default=':-P')

        self.register_for('joke')

    def on_tick(self) -> None:
        """Called every `_tick_interval` [s] while the process runs.

        Use this function if you have to do anything at regular
        intervals.

        If you only need to respond to events just register for the
        events in `on_init` and make sure you write the corresponding
        `on_EVENT` functions.
        """
        logger.debug('I\'m doing something immensely useful.')

    def on_joke(self, *values: str, **params: str) -> None:
        # pylint: disable=unused-argument
        """Gets called on event `joke`.

        Args:
            values: Values attached to the event (ignored).
            params: Parameters attached to the event (ignored).
        """
        logger.debug(self._smile)
