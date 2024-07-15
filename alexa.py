# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import requests
from requests.exceptions import Timeout
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ""
        reprompt_text = "¿Necesitas algo más?"

        try:
            response = requests.get('https://qq37ws9m-5000.use.devtunnels.ms/pruebita', timeout=60)
            if response.status_code == 200:
                speak_output = "¡Hola!, Bienvenido al negocio, ¿en qué puedo ayudarte hoy?"
            else:
                speak_output = "Hmmm hubo un error al conectarme a la base de datos de los clientes, intenta más tarde"
        except Timeout:
            speak_output = "Hmmm hubo un error al conectarme al sistema"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)  # Agrega esto para mantener la sesión abierta
                .response
        )

class GetCapitalIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("busqueda_capital_intent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = handler_input.request_envelope.request.intent.slots["nombres"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://qq37ws9m-5000.use.devtunnels.ms/api/obtener_estadoCliente'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class enviar_correo_intent(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("enviar_correo_intent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = handler_input.request_envelope.request.intent.slots["cliente"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://qq37ws9m-5000.use.devtunnels.ms/api/imprimir_pago_alexa'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class consultaPagoIntent(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("consultaPagoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = handler_input.request_envelope.request.intent.slots["cliente"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://qq37ws9m-5000.use.devtunnels.ms/api/obtener_pago'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Está bien, que pases un lindo día!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
        
        


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetCapitalIntentHandler())
sb.add_request_handler(enviar_correo_intent())
sb.add_request_handler(consultaPagoIntent())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()