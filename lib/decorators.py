import json
import functools
import traceback
from lib.utils import logger, parse_body


def api_handler(func):
    """APIのデコレータ."""
    @functools.wraps(func)
    def wrapper(event, context, email=None):
        logger.info(event)
        try:
            if event.get('body') is not None:
                event['body'] = parse_body(event.get('body'))
            return func(event, context)
        except TypeError:  # 入力がJSONでない場合
            return func(event, context)
        except json.decoder.JSONDecodeError:  # 入力がJSONでない場合
            return func(event, context)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
    return wrapper
