package main_test

import (
	v1 "prototest/proto/message/v1"
	v2 "prototest/proto/message/v2"
	"testing"

	"github.com/stretchr/testify/assert"
	"google.golang.org/protobuf/proto"
)

func TestProtoForwardCompatibility(t *testing.T) {
	v1ProtoMsg := &v1.EnvelopeV1{
		Sender: "First Person",
		Contents: &v1.EnvelopeV1_Message{
			Message: "hello world",
		},
	}

	v1ProtoMsgBytes, err := proto.Marshal(v1ProtoMsg)
	assert.NoError(t, err)

	v2ProtoMsg := new(v2.EnvelopeV2)
	err = proto.Unmarshal(v1ProtoMsgBytes, v2ProtoMsg)
	assert.NoError(t, err)
	assert.Equal(t, v1ProtoMsg.Sender, v2ProtoMsg.Sender)
	assert.Equal(t, v1ProtoMsg.GetMessage(), v2ProtoMsg.GetMessage())
}

func TestProtoBackwardCompatibility(t *testing.T) {
	// new message with old one-off message
	v2ProtoMsg := &v2.EnvelopeV2{
		Sender: "Second Person",
		Contents: &v2.EnvelopeV2_Message{
			Message: "hello world",
		},
	}

	v2ProtoMsgBytes, err := proto.Marshal(v2ProtoMsg)
	assert.NoError(t, err)

	v1ProtoMsg := new(v1.EnvelopeV1)
	err = proto.Unmarshal(v2ProtoMsgBytes, v1ProtoMsg)
	assert.NoError(t, err)
	assert.Equal(t, v1ProtoMsg.Sender, v2ProtoMsg.Sender)
	assert.Equal(t, v1ProtoMsg.GetMessage(), v2ProtoMsg.GetMessage())
	// new message with new one-off message
	v2ProtoMsg = &v2.EnvelopeV2{
		Sender: "Second Person",
		Contents: &v2.EnvelopeV2_EncodedImage{
			EncodedImage: "XXXXYYYY",
		},
	}

	v2ProtoMsgBytes, err = proto.Marshal(v2ProtoMsg)
	assert.NoError(t, err)

	v1ProtoMsg = new(v1.EnvelopeV1)
	err = proto.Unmarshal(v2ProtoMsgBytes, v1ProtoMsg)
	assert.NoError(t, err)
	assert.Equal(t, v1ProtoMsg.Sender, v2ProtoMsg.Sender)
	assert.Equal(t, v1ProtoMsg.GetMessage(), v2ProtoMsg.GetMessage())
}
